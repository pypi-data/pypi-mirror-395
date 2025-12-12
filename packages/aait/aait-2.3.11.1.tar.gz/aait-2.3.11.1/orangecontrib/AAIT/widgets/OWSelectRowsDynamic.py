import os
import sys

import Orange.data
from AnyQt.QtWidgets import QApplication
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
    from Orange.widgets.orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
else:
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file


@apply_modification_from_python_file(filepath_original_widget=__file__)
class OWSelectRowsDynamic(widget.OWWidget):
    name = "Select Rows Dynamic"
    description = "Select a row from a second entry"
    category = "AAIT - TOOLBOX"
    icon = "icons/select_dynamic_row.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/select_dynamic_row.png"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owselect_row_dynamic.ui")
    want_control_area = False
    priority = 1060

    class Inputs:
        data = Input("data", Orange.data.Table)
        data_for_filter = Input("input_for_filtering", Orange.data.Table)

    class Outputs:
        data_matching = Output("Matching Data", Orange.data.Table)
        data_unmatching = Output("UnMatching Data", Orange.data.Table)

    @Inputs.data
    def set_data(self, data_in):
        if data_in is None:
            return
        self.in_data = data_in
        if self.data_filter_in is None:
            return
        self.run()

    @Inputs.data_for_filter
    def set_path_table(self, in_data_filter):
        if in_data_filter is None:
            return

        total_columns = len(in_data_filter.domain.attributes) + len(in_data_filter.domain.class_vars) + len(
            in_data_filter.domain.metas)
        self.error("")
        if total_columns != 1:
            self.error("error filter_input can only use 1 column in this version")
            return
        if len(in_data_filter.domain.metas) != 1:
            self.error("error filter_input can only use Stringvariable")
            return
        if not isinstance(in_data_filter.domain.metas[0], Orange.data.StringVariable):
            self.error("error filter_input can only use Stringvariable.")
            return

        self.data_filter_in = in_data_filter
        if self.in_data is not None:
            self.run()

            # if total_columns != 1:
            #
            #     return
            #
            # print("in_data_filter")
            # print(in_data_filter)

    def __init__(self):
        super().__init__()
        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)
        self.data_filter_in = None
        self.in_data = None
        self.autorun = True
        self.post_initialized()

    def run(self):
        self.error("")
        # self.data_filter_in ne doit avoir qu'une colonne de type string (verifier en amiont)
        filter_var = self.data_filter_in.domain.metas
        filter_var_name = filter_var[0].name

        # Chercher la colonne correspondante dans in_data
        in_attrs = self.in_data.domain.metas
        match_vars = [var for var in in_attrs if
                      isinstance(var, Orange.data.StringVariable) and var.name == filter_var_name]

        if not match_vars:
            self.error(f"No column StringVariable  '{filter_var_name}' in in_data.")
            return

        match_var = match_vars[0]

        # Nettoyer les doublons dans data_filter_in et utiliser un set pour O(1) lookup
        values_filter_set = {
            str(row.metas[0]) for row in self.data_filter_in
            if row.metas[0] is not None
        }


        # Extract all values at once using list comprehension (faster than row-by-row)
        all_values = [row[match_var] for row in self.in_data]

        # Create boolean mask for matching rows
        matching_mask = [value in values_filter_set for value in all_values]

        # Use list comprehension with mask for filtering (much faster than appends in loop)
        matching_rows = [row for row, is_match in zip(self.in_data, matching_mask) if is_match]
        non_matching_rows = [row for row, is_match in zip(self.in_data, matching_mask) if not is_match]

        # Use more efficient table constructor
        if matching_rows:
            matched_table = Orange.data.Table(self.in_data.domain, matching_rows)
        else:
            matched_table = None

        if non_matching_rows:
            unmatched_table = Orange.data.Table(self.in_data.domain, non_matching_rows)
        else:
            unmatched_table = None

        # Sauvegarder les résultats dans l'objet widget si besoin
        self.Outputs.data_matching.send(matched_table)
        self.Outputs.data_unmatching.send(unmatched_table)

    def post_initialized(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWSelectRowsDynamic()
    my_widget.show()
    if hasattr(app, "exec"):
        app.exec()
    else:
        app.exec_()
