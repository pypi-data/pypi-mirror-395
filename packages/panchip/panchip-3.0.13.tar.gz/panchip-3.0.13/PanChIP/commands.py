import argparse
import textwrap
import sys

def panchip_parser():
    usage = '''\
        panchip <command> [options]
        Commands:
            init            Initialization of the PanChIP library
            analysis        Analysis of a list peak sets
            filter          Filtering library for quality control
        Run panchip <command> -h for help on a specific command.
        '''
    parser = argparse.ArgumentParser(
        description='PanChIP: Pan-ChIP-seq Analysis of Peak Sets',
        usage=textwrap.dedent(usage)
    )

    from .version import __version__
    parser.add_argument('--version', action='version', version=f'PanChIP {__version__}')
    
    parser.add_argument('command', nargs='?', help='Subcommand to run')

    return parser

def init_parser():
    parser = MyParser(
        description='Initialization of the PanChIP library',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='panchip init'
    )

    parser.add_argument(
        'library_directory',
        type=str,
        help='Directory wherein PanChIP library will be stored. > 13.6 GB of storage required.')

    return parser
      
def analysis_parser():
    parser = MyParser(
        description='Analysis of a list peak sets',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='panchip analysis'
    )
        
    parser.add_argument(
        'library_directory',
        type=str,
        help='Directory wherein PanChIP library was stored.')

    parser.add_argument(
        'input_directory',
        type=str,
        help='Input directory wherein peak sets in the format of .bed files are located.')
       
    parser.add_argument(
        'output_directory',
        type=str,
        help='Output directory wherein output files will be stored.')
    
    parser.add_argument(
        '-t',
        dest='threads',
        type=int,
        default=1,
        help='Number of threads to use.')
    
    parser.add_argument(
        '-r',
        dest='repeats',
        type=int,
        default=1,
        help='Number of repeats to perform.')

    return parser
        
def filter_parser():
    parser = MyParser(
        description='Filtering library for quality control',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='panchip filter'
    )
        
    parser.add_argument(
        'library_directory',
        type=str,
        help='Directory wherein PanChIP library was stored.')

    parser.add_argument(
        'input_file',
        type=str,
        help='Path to the input .bed file.')
       
    parser.add_argument(
        'output_directory',
        type=str,
        help='Output directory wherein output files will be stored.')
    
    parser.add_argument(
        '-t',
        dest='threads',
        type=int,
        default=1,
        help='Number of threads to use.')

    return parser
        
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
