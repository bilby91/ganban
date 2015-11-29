class JSON(object):
    def to_dict(self):
        dictionary = super(JSON, self).to_dict()
        if not self.key == None:
            dictionary['id'] = self.key.id()

        return dictionary
