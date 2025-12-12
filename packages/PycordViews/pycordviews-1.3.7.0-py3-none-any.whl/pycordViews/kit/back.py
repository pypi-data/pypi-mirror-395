from ..views.easy_modified_view import EasyModifiedViews

from typing import Optional, Union, Any, Callable
from discord.ui import Button
from discord import ButtonStyle, Role, Interaction
from inspect import currentframe

class Back:
    """
    Class
    -------------
    Allows you to easily setup a back button.
    He save function parameters when he is called and recall the function with these parameters.
    -------------
    """

    def __init__(self, timeout: Optional[float] = None,
                 disabled_on_timeout: bool = False,
                 row: int = 0,
                 autorised_roles: Optional[list[Union[Role, int]]] = None,
                 autorised_key: Optional[callable] = None):
        """
        Initialisation for back button
        """
        self.args_function: tuple = ()
        self.kwargs_function: dict = {}

        # get the calling function
        function_frame = currentframe().f_back
        call_function_frame = function_frame.f_back
        name = function_frame.f_code.co_name
        self.back_function: Union[Callable] = call_function_frame.f_globals.get(name) or call_function_frame.f_locals.get(name)

        self.__view = EasyModifiedViews(timeout=timeout, disabled_on_timeout=disabled_on_timeout)
        self.__view.add_items(Button(label='⏪ Back', row=row, custom_id='back', style=ButtonStyle.gray))
        self.__view.set_callable('back', _callable=self._back, autorised_roles=autorised_roles, autorised_key=autorised_key)

    def set_parameters(self, *args, **kwargs):
        """
        Set the parameters to recall the function
        :param args: The args to save
        :param kwargs: The kwargs to save
        """
        self.args_function = args
        self.kwargs_function = kwargs

    async def _back(self, button: Button, interaction: Interaction, data: dict[str, Any]):
        """
        Base asynchronous _back function called when button is pressed
        """
        await interaction.response.defer()
        await self.back_function(*self.args_function, **self.kwargs_function)

    def get_view(self) -> EasyModifiedViews:
        """
        Get the view with the back button
        :return: The view with the back button
        """
        return self.__view