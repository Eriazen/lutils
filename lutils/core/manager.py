import subprocess
from pathlib import Path

from lutils.core.data import FoamCase


class CaseManager:
    '''
    Manager class controlling OpenFOAM cases.
    Used to run or clean specified cases.
    '''
    def __init__(self,
                 cases: list[FoamCase]) -> None:
        '''
        Initialize CaseManager class.

        Parameters:
            - cases: list of FoamCase objects
        '''
        self.cases = {}
        for case in cases:
            self.cases[case.label] = case

    def load_of(self,
                of_bin: str) -> None:
        '''
        Loads given OpenFOAM version.

        Parameters:
            - of_bin: path to OpenFOAM binary
        '''
        subprocess.run(of_bin)

    def run_script(self,
                   script_name: str,
                   cases: list[str] | None = None) -> None:
        '''
        Runs arbitrary bash script on all or only specified OpenFOAM cases.

        Parameters:
            - script_name: name the script to be run, placed inside case directory
            - cases: list of case labels, None cleans all cases
        '''
        to_run = self._select_case(cases)

        pwd = Path.cwd()
        for case in to_run:
            print(pwd / case._case_path)
            subprocess.run(f'./{script_name}', cwd= pwd / case._case_path)

    def _select_case(self,
                     cases: list[str] | None = None) -> list[FoamCase]:
        '''
        Utility method used to select specified cases from self.cases dictionary.

        Parametrs:
            - cases: list of case labels, None selects all cases
        '''
        if not cases:
            selected = [self.cases[label] for label in self.cases.keys()]
        else:
            selected = [self.cases[label] for label in cases]
        return selected

    def add_case(self,
                 case: FoamCase) -> None:
        '''
        Adds specified case to manager dictionary under its label.
        '''
        self.cases[case.label] = case
