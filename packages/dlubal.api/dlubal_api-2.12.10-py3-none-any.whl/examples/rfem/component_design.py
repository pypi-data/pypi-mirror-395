from dlubal.api import rfem, common
from typing import List, Dict
import pandas


class DesignCheck:

    def __init__(self, app: rfem.Application, component_no: int, loading: str):

        self.app = app
        self.component_no = component_no
        self.loading = loading

        self.checks = pandas.DataFrame()

    def define_design_checks(self) -> List[Dict]:
        """
        Returns a list of design checks for this component.
        Each check can have a different description and parameters.
        """
        # Define multiple checks for the same component
        return [
            {"type": "CP-10.001", "description": "Ultimate Limit State | Load Capacity on F1", "category": "ULS", "subcategory": "Capacity"},
            {"type": "CP-10.002", "description": "Ultimate Limit State | Load Capacity on F3", "category": "ULS", "subcategory": "Capacity"},
        ]


    def parse_member_location(self, member_location: str) -> {int, str}:
        if member_location[-1] in ['E', 'S']:
            return int(member_location[:-1]), member_location[-1]
        return int(member_location), 'B'


    def evaluate_design_check(self): # -> pandas.DataFrame:

        """
        Perform the specific design check based on the 'check' dictionary passed in.
        """

        component: rfem.component_design_objects.Component  = self.app.get_object(
            rfem.component_design_objects.Component(no=self.component_no)
        )
        print(component)

        nail_type = common.get_tree_value(
            tree=component.component_settings,
            path=["fastening", "nail_type", "nail_type_nail_type"]
        )

        results = self.app.get_results(
            results_type=rfem.results.STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES,
        ).data

        design_check_types = []

        member_ends = [m.strip() for m in component.assigned_to_member_ends.split(',')]

        for member_end in member_ends:

            member_no, location = self.parse_member_location(member_end)

            member: rfem.structure_core.Member = self.app.get_object(
                rfem.structure_core.Member(no=member_no)
            )

            nodes = []
            if location in ['S', 'B']:  # S=start, 3=Both
                nodes.append((member.node_start, "S"))
            if location in ['E', 'B']:  # E=end, 3=Both
                nodes.append((member.node_end, "E"))

            for node_no, assignment in nodes:
                print(node_no)

                forces = results[
                    (results['member_no'] == member_no) &
                    (results['node_no'] == node_no) &
                    (results['loading'] == self.loading)
                ]
                print(forces)

                checks_definition = self.define_design_checks()

                for check in checks_definition:

                    check_type = check["type"]
                    check_description = check["description"]

                    # Define design check for each check type  Fd / Rd
                    if check_type == "CP-10.001": # F1 = Vz
                        applied_force = forces['v_z'].abs().max() / 1000    # kN
                        print(applied_force)
                        if nail_type == "Full Nailing":
                            capacity = common.get_tree_value(
                                tree=component.component_parameters,
                                path=["characteristic_capacities", "full_nailing", "load_capacity_on_f1_r_1_k_cna4_0x40"]
                            )
                        else:
                            capacity = common.get_tree_value(
                                tree=component.component_parameters,
                                path=["characteristic_capacities", "partial_nailing", "load_capacity_on_f1_r_1_k_cna4_0x40"]
                            )
                        design_ratio = (applied_force / float(capacity)) # * gamma_m

                    elif check_type == "CP-10.002": # F3 = Vy
                        applied_force = forces['v_y'].abs().max() / 1000    # kN
                        print(applied_force)
                        if nail_type == "Full Nailing":
                            capacity = common.get_tree_value(
                                tree=component.component_parameters,
                                path=["characteristic_capacities", "full_nailing", "load_capacity_on_f3_r_3_k_cna4_0x40"]
                            )
                        else:
                            capacity = common.get_tree_value(
                                tree=component.component_parameters,
                                path=["characteristic_capacities", "partial_nailing", "load_capacity_on_f3_r_3_k_cna4_0x40"]
                            )
                        design_ratio = (applied_force / float(capacity)) # * gamma_m

                    else:
                        design_ratio = 3.0

                    design_check_types.append({
                        "Component No.": component.no,
                        "Member No.": member_no,
                        "Assignment": assignment,
                        "Node No.": node_no,
                        "Loading": self.loading,
                        "Applied Force": applied_force,         #kN
                        "Capacity": capacity,                   #kN
                        "Ratio": design_ratio,
                        "Type": check_type,
                        "Description": check_description,
                    })

        self.checks = pandas.concat([self.checks, pandas.DataFrame(design_check_types)])
        return self.checks



if __name__ == "__main__":

    rfem_app = rfem.Application()

    try:
        design_check = DesignCheck(
            app=rfem_app,
            component_no=1,
            loading='CO3'
        )

        design_check_df = design_check.evaluate_design_check()

        print("\nDesign Check:")
        print(design_check_df.to_string(index=False))

        rfem_app.close_connection()

    except Exception as e:
        rfem_app.close_connection()
        print(f"Error: {e}")