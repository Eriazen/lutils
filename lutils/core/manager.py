from lutils.core.data import FoamCase


class CaseManager:
    '''
    Manager class controlling OpenFOAM cases.
    Used to run or clean specified cases.
    '''

    def __init__(self,
                 case_paths: list[str],
                 case_labels: list[str]) -> None:
        '''
        Initialize CaseManager class.

        Parameters:
            - case_paths: list of paths to OpenFOAM case directories
            - case_labels: list of unique case labels used to reference individual cases
        '''
        self.cases = {}
        # load each case into dict
        for path, label in zip(case_paths, case_labels):
            self.add_case_by_path(path, label)

    def run_script(self,
                   file_name: str,
                   case_labels: list[str] | None = None) -> None:
        '''
        Runs an arbitrary script on selected OpenFOAM cases.

        Parameters:
            - file_name: path to script, relative paths are assumed to be inside the case directory
            - case_labels: list of case labels, None runs the script on all cases
        '''
        # select cases based on input
        if not case_labels:
            cases = list(self.cases.values())
        else:
            cases = [self.cases[label] for label in case_labels]
        # run script from case directory
        for case in cases:
            case.run_script(file_name)

    def add_case_by_path(self,
                         path: str,
                         case_label: str) -> None:
        '''
        Adds specified case to manager dictionary under its label.

        Parameters:
            - path: path to main OpenFOAM case directory
            - case_label: unique case label used to reference this case
        '''
        try:
            case = FoamCase(path, case_label)

        except (FileNotFoundError, OSError, ValueError) as e:
            raise ValueError(
                f'Error adding case to manager. Invalid path or internal FoamCase creation failes.'
                f'Check path: {path}.'
            ) from e

        if case_label in self.cases:
            raise ValueError(
                f'Unique Label Error: A case with label "{case_label}" already in the manager!')
        self.cases[case.label] = case
