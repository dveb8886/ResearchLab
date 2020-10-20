import general.settings as settings


class BaseMdl:

    def get_resource(self):
        raise NotImplementedError('get_resource has not been implemented for this model')

