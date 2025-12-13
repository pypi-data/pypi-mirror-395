from gig.core.GIGTable import GIGTable


class EntGIGMixin:
    def gig(self, gig_table: GIGTable):
        return gig_table.get(self.id)
