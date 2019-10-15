from .media import Media
import textwrap


class Story(Media):

    skip_prop = [
        'owner'
    ]

    #  We do not need some values - do not parse it for Story,
    #  for example - we do not need owner object inside story
     
    #  param value
    #  param prop
    #  param arr

    def _init_properties_custom(self, value, prop, arr):
        if prop in Story.skip_prop:
            return
        
        super()._init_properties_custom(value, prop, arr)

    def __str__(self):
        string = f"""
        Story Info:
        'Id: {self.identifier}
        Hig res image: {self.image_high_resolution_url}
        Media type: {self.type if hasattr(self, 'type') else ''}
        """
        
        return textwrap.dedent(string)
