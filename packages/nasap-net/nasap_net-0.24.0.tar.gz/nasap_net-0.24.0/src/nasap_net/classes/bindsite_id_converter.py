__all__ = ['BindsiteIdConverter']


class BindsiteIdConverter:
    DELIMITER = '.'

    def local_to_global(self, comp_id: str, local_bs_id: str) -> str:
        return f'{comp_id}{self.DELIMITER}{local_bs_id}'

    def global_to_local(self, abs_bs_id: str) -> tuple[str, str]:
        splited = abs_bs_id.split(self.DELIMITER)
        assert len(splited) == 2
        comp_id, local_bs_id = splited
        return comp_id, local_bs_id
