import io
import numpy as np
from .visualization import RenderOutput
from .report import ReportEntry, ReportContext

try:
    import luminarycloud_jupyter as lcj
except ImportError:
    lcj = None


def _detect_outliers(
    metadata: list[dict[str, str | float]],
    output_fields: list[str],
    percentile_threshold: float = 95.0,
) -> list[int] | None:
    """
    Detect outliers using Mahalanobis distance.

    Parameters
    ----------
    metadata : list[dict[str, str | float]]
        List of metadata dictionaries for each row
    output_fields : list[str]
        List of output field names to use for outlier detection
    percentile_threshold : float, optional
        Percentile threshold for outlier detection (default: 95.0)

    Returns
    -------
    list[int] | None
        List of row indices that are outliers, or None if detection fails
    """
    # Need at least 2 fields for meaningful multivariate analysis
    if len(output_fields) < 2:
        return None

    # Extract data for the specified output fields
    try:
        data = []
        for row_metadata in metadata:
            row_data = []
            for field in output_fields:
                value = row_metadata.get(field)
                if value is None or isinstance(value, str):
                    # Skip if field is missing or non-numeric
                    return None
                row_data.append(float(value))
            data.append(row_data)

        data_array = np.array(data)

        # Need at least as many samples as dimensions for covariance matrix
        if len(data_array) < len(output_fields):
            return None

        # Calculate mean and covariance matrix
        mean_vec = np.mean(data_array, axis=0)
        cov_matrix = np.cov(data_array.T)

        # Check if covariance matrix is singular
        if np.linalg.det(cov_matrix) == 0:
            return None

        # Invert covariance matrix
        inv_cov_matrix = np.linalg.inv(cov_matrix)

        # Calculate Mahalanobis distance for each point
        distances = []
        for point in data_array:
            diff = point - mean_vec
            distance = np.sqrt(diff @ inv_cov_matrix @ diff)
            distances.append(distance)

        # Determine outlier threshold using percentile
        threshold = np.percentile(distances, percentile_threshold)

        # Find outlier indices
        outlier_indices = [i for i, d in enumerate(distances) if d > threshold]

        return outlier_indices

    except Exception:
        # If anything goes wrong, return None (no outliers detected)
        return None


class InteractiveReport:
    """
    Interactive report widget with lazy loading for large datasets.

    How it works:
    1. on initialization:
       - sends metadata for all rows (for filtering/selection)
       - downloads the first row (to determine grid dimensions)
       - other rows remain unloaded

    2. on user request:
       - _load_row_data() is called with row index
       - downloads and sends images/plots for that specific row
       - python sets row_states to 'loading' -> 'loaded' (or 'error')

    This allows working with 1000+ row datasets without waiting for all data upfront.
    """

    # TODO Will/Matt: this list of report entries could be how we store stuff in the DB
    # for interactive reports, to reference the post proc. extracts. A report is essentially
    # a bunch of extracts + metadata.
    def __init__(self, entries: list[ReportEntry], context: ReportContext | None = None) -> None:
        if not lcj:
            raise ImportError("InteractiveScene requires luminarycloud[jupyter] to be installed")

        self.entries = entries
        if len(self.entries) == 0:
            raise ValueError("Invalid number of entries, must be > 0")

        # Validate and store context if provided
        if context is not None:
            self._validate_context(context)
            self.context = context
        else:
            self.context = None

        # Determine grid dimensions by downloading first entry
        # to understand the structure (number of columns)
        first_entry = self.entries[0]
        first_entry.download_extracts()

        # Calculate actual number of columns by counting how many cells
        # each extract produces (RenderOutput can produce multiple images)
        ncols = 0
        for extract in first_entry._extracts:
            if isinstance(extract, RenderOutput):
                image_and_label = extract.download_images()
                ncols += len(image_and_label)
            else:
                ncols += 1  # Plot data extracts produce one cell

        nrows = len(self.entries)

        # Prepare report context for the widget
        context_dict = None
        if self.context is not None:
            context_dict = self.context.to_dict()

            # Compute outlier indices if we have outputs
            if self.context.outputs and len(self.context.outputs) >= 2:
                outlier_indices = _detect_outliers(
                    [re._metadata for re in self.entries], self.context.outputs
                )
                if outlier_indices is not None:
                    context_dict["outlier_indices"] = outlier_indices

        # Create widget with metadata but without data
        self.widget = lcj.EnsembleWidget(
            [re._metadata for re in self.entries], nrows, ncols, report_context=context_dict
        )

        # Set the callback for lazy loading row data
        self.widget.set_row_data_callback(self._load_row_data)

    def _validate_context(self, context: ReportContext) -> None:
        """
        Validate that all inputs and outputs from the ReportContext exist in the
        first report entry's metadata.

        Raises:
        -------
        ValueError
            If any inputs or outputs are missing from the first entry's metadata.
        """
        first_entry = self.entries[0]
        metadata_keys = set(first_entry._metadata.keys())

        # Check for missing inputs
        missing_inputs = [key for key in context.inputs if key not in metadata_keys]

        # Check for missing outputs
        missing_outputs = [key for key in context.outputs if key not in metadata_keys]

        # Raise exception if any keys are missing
        if missing_inputs or missing_outputs:
            error_parts = []
            if missing_inputs:
                error_parts.append(f"Missing inputs: {missing_inputs}")
            if missing_outputs:
                error_parts.append(f"Missing outputs: {missing_outputs}")
            raise ValueError(f"ReportContext validation failed. {', '.join(error_parts)}")

    def _load_row_data(self, row: int) -> None:
        """
        Load and send data for a specific row to the widget.
        This is called on-demand when the user requests data for a row.
        """
        re = self.entries[row]

        # Download extracts if not already downloaded
        if len(re._extracts) == 0:
            re.download_extracts()

        # Process each extract and send to widget
        # Track the actual column index as we may have multiple cells per extract
        col = 0
        for extract in re._extracts:
            if isinstance(extract, RenderOutput):
                image_and_label = extract.download_images()
                # Each image gets its own column
                for il in image_and_label:
                    # il is a tuple of (BytesIO, label)
                    # Use camera label for the name, fallback to "image" if empty
                    camera_label = il[1]
                    name = camera_label if camera_label else "image"
                    # For description: prefer extract.description, then camera label, then fallback message
                    description = (
                        extract.description
                        if extract.description
                        else camera_label if camera_label else "no label or description provided"
                    )
                    self.widget.set_cell_data(
                        row,
                        col,
                        il[0].getvalue(),
                        "jpg",
                        name=name,
                        description=description,
                    )
                    col += 1
            else:
                plot_data = extract.download_data()
                data = plot_data[0][0]  # The CSV data (rows)
                plot_label = plot_data[0][1]  # The label from the extract
                all_axis_labels = data[0]

                axis_data = []
                for axis_idx in range(len(all_axis_labels)):
                    axis_values = [row[axis_idx] for row in data[1:]]
                    axis_data.append(axis_values)

                # For plots: use extract.name, then plot_label, then "plot" as fallback
                # For description: use extract.description, fallback to message if empty
                name = extract.name if extract.name else (plot_label if plot_label else "plot")
                description = (
                    extract.description
                    if extract.description
                    else "no label or description provided"
                )

                self.widget.set_cell_scatter_plot(
                    row,
                    col,
                    name,  # Use the same name for the plot title
                    all_axis_labels,
                    axis_data,
                    plot_name=name,
                    plot_mode="markers",
                    name=name,
                    description=description,
                )
                col += 1

    def _ipython_display_(self) -> None:
        """
        When the InteractiveReport is shown in Jupyter we show the underlying widget
        to run the widget's frontend code
        """
        self.widget._ipython_display_()
