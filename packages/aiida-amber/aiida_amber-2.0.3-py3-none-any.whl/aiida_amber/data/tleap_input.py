"""Sub class of `Data` to handle inputs used and outputs that will be produced
from commands in the tleap input file."""
import re
import os
import sys
from aiida.orm import SinglefileData, FolderData, List
from aiida_amber.utils import node_utils


class TleapInputData(SinglefileData):
    """Class to find the inputs used and outputs produced from
    the commands in the tleap input file"""

    def set_file(self, file, filename=None, **kwargs):
        """Add a file to the node, parse it and set the attributes found.

        :param file: absolute path to the file or a filelike object
        :param filename: specify filename to use (defaults to name of provided file).
        """
        super().set_file(file, filename, **kwargs)

        # Parse the tleap file
        parsed_info = parse_tleap_input_file(self.get_content().splitlines())

        # Add all other attributes found in the parsed dictionary
        for key, value in parsed_info.items():
            self.base.attributes.set(key, value)

    @property
    def inpfile_list(self):
        """Return the list input files used in the tleap script
        """
        return self.base.attributes.get('input_files')
    
    @property
    def outfile_list(self):
        """Return the list output files to be produced from the tleap script
        """
        return self.base.attributes.get('output_files')

    @property
    def calculation_inputs_outputs(self):
        """Return the inputs for the tleap calculation job
        """
        input_files = self.inpfile_list
        subdirs, files = node_utils.check_filepath(input_files)
        calc_inputs = add_calculation_inputs(subdirs, files)
        output_files = self.outfile_list
        calc_outputs = add_calculation_outputs(output_files)
        return calc_inputs, calc_outputs


def parse_tleap_input_file(lines):
    """Parse tleap script and find any instances of file loads (inputs)
    or saves (outputs)
    """
    input_files = []
    output_files = []
    # iterate through tleap lines and find input and output files
    for line in lines:
        head, sep, tail = line.partition("#")
        # if "load" string in line then find input file
        if re.search("load", head, re.IGNORECASE):
            split_line = head.split()
            if len(split_line) > 2:
                if "load" in split_line[-2]:
                    input_files.append(split_line[-1])
            if "load" in split_line[0]:
                input_files.append(split_line[1])
        # if "save" string in line then find output file
        if re.search("save", head, re.IGNORECASE):
            if re.search("saveAmberParm", head, re.IGNORECASE):
                output_files.extend(head.split()[-2:])
            else:
                output_files.append(head.split()[2])
        if re.search("logFile", head, re.IGNORECASE):
            output_files.append(head.split()[-1])

    parsed_info = {}
    parsed_info["input_files"] = input_files
    parsed_info["output_files"] = output_files

    return parsed_info


def add_calculation_inputs(subdirs, files):
    """If they exist, add input files for tleap and dirs into the calcjob 
    inputs directory
    """
    calc_inputs = {}
    input_list = []
    # If we have tleap input files then tag them.
    if files:
        calc_inputs["tleap_inpfiles"] = {}
        # Iterate files to assemble a dict of names and paths.
        for file in files:
            formatted_filename = node_utils.format_link_label(file)
            if os.path.isfile(file):
                input_list.append(file)
                calc_inputs["tleap_inpfiles"][formatted_filename] = \
                    SinglefileData(file=os.path.join(os.getcwd(), file))

            elif "PYTEST_CURRENT_TEST" in os.environ:
                test_path = os.path.join(os.getcwd(), 
                                        'tests/input_files/tleap', file)
                if os.path.isfile(test_path):
                    calc_inputs["tleap_inpfiles"][formatted_filename] = \
                        SinglefileData(file=test_path)
                else:
                    sys.exit(f"Error: Input file {file} referenced in tleap file does not exist")

            
            else:
                sys.exit(f"Error: Input file {file} referenced in tleap file does not exist")

    # If we have included files in subdirs then process these.

    if subdirs:
        calc_inputs["tleap_dirs"] = {}
        # for each entry establish dir path and build file tree.
        for subdir in subdirs:
            if os.path.isfile(subdir):
                # add file to input list
                input_list.append(subdir.split("/")[-1])
                frst_dir = subdir.split("/")[0]
                # Create a folder that is empty.
                if frst_dir not in calc_inputs["tleap_dirs"].keys():
                    calc_inputs["tleap_dirs"][frst_dir] = FolderData()
                # Now fill it with files referenced in the tleap inputfile.
                # need to make sure to include any nested dirs in the path
                calc_inputs["tleap_dirs"][frst_dir].put_object_from_file(
                    os.path.join(os.getcwd(), subdir), 
                    path="/".join(subdir.split("/")[1:]) # remove the first dir
                    )
                
            # For tests
            elif "PYTEST_CURRENT_TEST" in os.environ:
                if os.path.isfile(os.path.join(os.getcwd(), "tests", subdir)):
                    # Create a folder that is empty.
                    if "tests" not in calc_inputs["tleap_dirs"].keys():
                        calc_inputs["tleap_dirs"]["tests"] = FolderData()
                    # Now fill it with files referenced in the tleap inputfile.
                    calc_inputs["tleap_dirs"]["tests"].put_object_from_file(
                        os.path.join(os.getcwd(), "tests", subdir), 
                        path=subdir)
                        
            else:
                sys.exit(f"Error: subdir {subdir} referenced in tleap file does not exist")

    # NOTE: this list is not used at the moment, might use for searchprevious
    calc_inputs["input_list"] = List(input_list)

    return calc_inputs


def add_calculation_outputs(files):
    """Add outputs from tleap script
    """
    calc_outputs = {}
    # If we have tleap output files then tag them.
    if files:
        output_list = []
        # Iterate files to assemble a dict of names and paths.
        for file in files:
            if "/" in file:
                file = file.split("/")[-1]
            output_list.append(file)
        calc_outputs["tleap_outfiles"] = List(output_list)
    return calc_outputs
                  
