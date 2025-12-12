"""
Calculations provided by aiida_amber.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
import os

from aiida.common import CalcInfo, datastructures
from aiida.engine import CalcJob
from aiida.orm import List, SinglefileData
from aiida.plugins import DataFactory

Pdb4amberParameters = DataFactory("amber.pdb4amber")


class Pdb4amberCalculation(CalcJob):
    """
    AiiDA calculation plugin wrapping the pdb4amber executable.

    AiiDA plugin wrapper for the amber 'pdb4amber' command.
    """

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super().define(spec)

        # set default values for AiiDA options
        spec.inputs['metadata']['options']['withmpi'].default = False
        spec.inputs["metadata"]["options"]["resources"].default = {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        }

        # required inputs
        spec.inputs["metadata"]["options"]["parser_name"].default = "amber.pdb4amber"
        spec.input('metadata.options.output_filename', valid_type=str,
                   default='pdb4amber.out', help='name of file stdout produced by default.')
        spec.input('metadata.options.output_dir', valid_type=str, default=os.getcwd(),
                help='Directory where output files will be saved when parsed.')
        spec.input('parameters', valid_type=Pdb4amberParameters,
                   help='Command line parameters for pdb4amber')
        spec.input("input_file", valid_type=SinglefileData,
                   help="input pdb file for pdb4amber")

        # no optional inputs

        # required outputs
        spec.output('stdout', valid_type=SinglefileData, help='stdout')
        spec.output('output_file', valid_type=SinglefileData, help='outputted pdb file')

        # optional outputs are saved as a list
        # set the list of output file names as an input so that it can be
        # iterated over in the parser later.
        spec.input('pdb4amber_outfiles', valid_type=List, required=False,
                   help='List of pdb4amber output file names.')

        # IMPORTANT:
        # Use spec.outputs.dynamic = True to make the entire output namespace
        # fully dynamic. This means any number of output files
        # can be linked to a node.
        spec.outputs.dynamic = True
        spec.inputs.dynamic = True
        spec.inputs['metadata']['options'].dynamic = True

        spec.exit_code(300, "ERROR_MISSING_OUTPUT_FILES",
            message="Calculation did not produce all expected output files.")

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should
            temporarily place all files needed by the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()

        # Setup data structures for files.
        # Any input files used
        input_options = [
            "input_file",
        ]
        # Any output files produced
        cmdline_input_files = {}
        input_files = []
        output_files = []

        # Map input files to AiiDA plugin data types.
        for item in input_options:
            if item in self.inputs:
                cmdline_input_files[item] = self.inputs[item].filename
                input_files.append(
                    (
                        self.inputs[item].uuid,
                        self.inputs[item].filename,
                        self.inputs[item].filename,
                    )
                )

        # Add output files to retrieve list.
        output_files.append(self.metadata.options.output_filename)
        if "pdb4amber_outfiles" in self.inputs:  # check there are output files.
            for name in self.inputs.pdb4amber_outfiles:
                output_files.append(str(name))  # save output filename to list

        # Form the commandline.
        codeinfo.cmdline_params = self.inputs.parameters.cmdline_params(
            cmdline_input_files
        )

        codeinfo.code_uuid = self.inputs.code.uuid
        # set stdout as the name set for -o flag
        codeinfo.stdout_name = self.metadata.options.output_filename
        codeinfo.withmpi = self.inputs.metadata.options.withmpi

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = CalcInfo()
        calcinfo.codes_info = [codeinfo]
        calcinfo.local_copy_list = input_files
        calcinfo.retrieve_list = output_files

        return calcinfo
