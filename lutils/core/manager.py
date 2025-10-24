import subprocess
from pathlib import Path

from .data import FoamCase


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

    def run_case(self,
                 cases: list[str] | None = None):
        '''
        Runs all or specified OpenFOAM cases.

        Parameters:
            - cases: list of case labels, None runs all cases
        '''
        to_run = self._select_case(cases)
        
        pwd = Path.cwd()
        for case in to_run:
            subprocess.run('./Allrun', cwd= pwd / case._case_path)

    def clean_case(self,
                   cases: list[str] | None = None) -> None:
        '''
        Cleans all or specified OpenFOAM cases.

        Parameters:
            - cases: list of case labels, None cleans all cases
        '''
        to_clean = self._select_case(cases)
        
        pwd = Path.cwd()
        for case in to_clean:
            print(pwd / case._case_path)
            subprocess.run('./Allclean', cwd= pwd / case._case_path)

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
