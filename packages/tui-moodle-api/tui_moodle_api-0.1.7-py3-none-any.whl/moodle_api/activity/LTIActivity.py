from .Activity import Activity


class LTIActivity(Activity):
    async def set_tool_url(self, tool_url: str, save: bool = False):
        return await self._set(save, toolurl=tool_url)

    # TODO typeid
