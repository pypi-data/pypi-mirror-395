import click

from nasap_net.cli.commands import (run_concat_assembly_lists_pipeline,
                                    run_enum_assemblies_pipeline,
                                    run_explore_reactions_pipeline)


@click.group()
@click.version_option(prog_name='nasap_net')
def main():
    """NASAPNet CLI"""
    pass

main.add_command(run_concat_assembly_lists_pipeline)
main.add_command(run_enum_assemblies_pipeline)
main.add_command(run_explore_reactions_pipeline)
