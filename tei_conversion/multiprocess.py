from multiprocessing import Pool
import argparse, os
import yaml
from pathlib import Path
from time import perf_counter
import glob
from src.build import TEI
from src.write_output import Write

def file_path(string):
    """Verify if the string passed as the argument --config is a valid file path.

    Args:
        string (str): file path to YAML configuration file.

    Raises:
        FileNotFoundError: informs user that the file path is invalid.

    Returns:
        (str): validated path to configuration file
    """    
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def get_args():
    """Parse command-line arguments and verify (1) the config file exist, (2) the TEI elements demanded can be constructed.
    """    
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", nargs=1, type=file_path, required=True,
                        help="path to the YAML configuration file")
    parser.add_argument("--version", nargs=1, type=str, required=True,
                        help="version of Kraken used to create the ALTO-XML files")
    parser.add_argument("--header", default=False, action='store_true',
                        help="produce TEI-XML with <teiHeader>")
    parser.add_argument("--sourcedoc", default=False, action='store_true',
                        help="produce TEI-XML with <sourceDoc>")
    parser.add_argument("--body", default=False, action='store_true',
                        help="produce TEI-XML with <body>")
    args = parser.parse_args()
    if args.body and not args.sourcedoc: 
        print("Cannot produce <body> without <sourceDoc>.\nTo call the program with the --body option, include also the --sourcedoc option.")
    return args.config, args.version, args.header, args.sourcedoc, args.body

def altos2tei_multiprocess(directory):
    #Get value of arguments (mainly path to config)
    config, version, header, sourcedoc, body = get_args()
    #load info from yaml file
    with open(config[0]) as cf_file:
        config = yaml.safe_load(cf_file.read())
    #get working directory where the data are
    working_dir=Path(config.get(("data"))["path"])
    #get path to all the XMLs to process
    altos = glob.glob(os.path.join(working_dir,directory, '*.xml'))
    print("Doc being processed")
    # instantiate the class TEI for the current document in the loop
    tree = TEI(directory, altos)
    tree.build_tree()
    print("\n=====================================")
    print(f"\33[32m~ now processing document {directory} ~\x1b[0m")
    #we build the header with info from the config file and a template
    if header:
        print(f"\33[33mbuilding <teiHeader>\x1b[0m")
        t0 = perf_counter()
        tree.build_header(config, version[0])
        print("|________finished in {:.4f} seconds".format(perf_counter() - t0))
    #we build the sourcedoc of the TEI file
    if sourcedoc:
        print(f"\33[33mbuilding <sourceDoc>\x1b[0m")
        t0 = perf_counter()
        tree.build_sourcedoc()
        print("|________finished in {:.4f} seconds".format(perf_counter() - t0))
    #we build the body of the TEI file
    if body:
        print(f"\33[33mbuilding <body>\x1b[0m")
        t0 = perf_counter()
        tree.build_body()
        print("|________finished in {:.4f} seconds".format(perf_counter() - t0))
    
    #we get the absolute path of the current working directory (important when multiprocessing)
    current_working_directory = Path.cwd()
    #we save the XML-TEI file in the data folder
    Write(os.path.join(current_working_directory,'data',directory), tree.root).write()
    print("XML-TEI file saved in data folder.")

if __name__ == '__main__':
    #get current dir
    current_working_directory = Path.cwd()
    #create dir called "data" to store TEI
    if not os.path.exists(os.path.join(current_working_directory,'data')):
        os.makedirs(os.path.join(current_working_directory,'data'))

    #get the list of all the pdfs
    config, version, header, sourcedoc, body = get_args()
    with open(config[0]) as cf_file:
        config = yaml.safe_load(cf_file.read())

    # for every directory in the path indicated in the configuration file,
    # get the directory's name (str) and the paths of its ALTO files (os.path)
    folder=Path(config.get(("data"))["path"])
    directories = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

    #We parallelise
    pool = Pool(processes=12)

    print("It starts")
    
    pool.map(altos2tei_multiprocess, directories)
