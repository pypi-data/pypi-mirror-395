import typing
from typing import Literal

import shadowlib.utilities.timing as timing
from shadowlib.globals import getClient

# --- All 64 widget fields as a Literal union -----------------------------

WidgetField = Literal[
    "getActions",
    "getAnimationId",
    "getBorderType",
    "getBounds",
    "getCanvasLocation",
    "getClickMask",
    "getContentType",
    "getDragDeadTime",
    "getDragDeadZone",
    "getDragParent",
    "getFont",
    "getFontId",
    "getHeight",
    "getHeightMode",
    "getId",
    "getIndex",
    "getItemId",
    "getItemQuantity",
    "getItemQuantityMode",
    "getLineHeight",
    "getModelId",
    "getModelType",
    "getModelZoom",
    "getName",
    "getNoClickThrough",
    "getNoScrollThrough",
    "getOnInvTransmitListener",
    "getOnKeyListener",
    "getOnLoadListener",
    "getOnOpListener",
    "getOnVarTransmitListener",
    "getOpacity",
    "getOriginalHeight",
    "getOriginalWidth",
    "getOriginalX",
    "getOriginalY",
    "getParent",
    "getParentId",
    "getRelativeX",
    "getRelativeY",
    "getRotationX",
    "getRotationY",
    "getRotationZ",
    "getScrollHeight",
    "getScrollWidth",
    "getScrollX",
    "getScrollY",
    "getSpriteId",
    "getSpriteTiling",
    "getStaticChildren",
    "getTargetPriority",
    "getTargetVerb",
    "getText",
    "getTextColor",
    "getTextShadowed",
    "getType",
    "getVarTransmitTrigger",
    "getWidth",
    "getWidthMode",
    "getXPositionMode",
    "getXTextAlignment",
    "getYPositionMode",
    "getYTextAlignment",
    "hasListener",
]


# --- Autocomplete helper -------------------------------------------------


class _WidgetFields:
    """
    Provides autocomplete for widget field names.

    Usage:
        w = Widget(id)
        w.enable(WidgetFields.getBounds)  # IDE autocomplete works!
    """

    getActions: WidgetField = "getActions"
    getAnimationId: WidgetField = "getAnimationId"
    getBorderType: WidgetField = "getBorderType"
    getBounds: WidgetField = "getBounds"
    getCanvasLocation: WidgetField = "getCanvasLocation"
    getClickMask: WidgetField = "getClickMask"
    getContentType: WidgetField = "getContentType"
    getDragDeadTime: WidgetField = "getDragDeadTime"
    getDragDeadZone: WidgetField = "getDragDeadZone"
    getDragParent: WidgetField = "getDragParent"
    getFont: WidgetField = "getFont"
    getFontId: WidgetField = "getFontId"
    getHeight: WidgetField = "getHeight"
    getHeightMode: WidgetField = "getHeightMode"
    getId: WidgetField = "getId"
    getIndex: WidgetField = "getIndex"
    getItemId: WidgetField = "getItemId"
    getItemQuantity: WidgetField = "getItemQuantity"
    getItemQuantityMode: WidgetField = "getItemQuantityMode"
    getLineHeight: WidgetField = "getLineHeight"
    getModelId: WidgetField = "getModelId"
    getModelType: WidgetField = "getModelType"
    getModelZoom: WidgetField = "getModelZoom"
    getName: WidgetField = "getName"
    getNoClickThrough: WidgetField = "getNoClickThrough"
    getNoScrollThrough: WidgetField = "getNoScrollThrough"
    getOnInvTransmitListener: WidgetField = "getOnInvTransmitListener"
    getOnKeyListener: WidgetField = "getOnKeyListener"
    getOnLoadListener: WidgetField = "getOnLoadListener"
    getOnOpListener: WidgetField = "getOnOpListener"
    getOnVarTransmitListener: WidgetField = "getOnVarTransmitListener"
    getOpacity: WidgetField = "getOpacity"
    getOriginalHeight: WidgetField = "getOriginalHeight"
    getOriginalWidth: WidgetField = "getOriginalWidth"
    getOriginalX: WidgetField = "getOriginalX"
    getOriginalY: WidgetField = "getOriginalY"
    getParent: WidgetField = "getParent"
    getParentId: WidgetField = "getParentId"
    getRelativeX: WidgetField = "getRelativeX"
    getRelativeY: WidgetField = "getRelativeY"
    getRotationX: WidgetField = "getRotationX"
    getRotationY: WidgetField = "getRotationY"
    getRotationZ: WidgetField = "getRotationZ"
    getScrollHeight: WidgetField = "getScrollHeight"
    getScrollWidth: WidgetField = "getScrollWidth"
    getScrollX: WidgetField = "getScrollX"
    getScrollY: WidgetField = "getScrollY"
    getSpriteId: WidgetField = "getSpriteId"
    getSpriteTiling: WidgetField = "getSpriteTiling"
    getStaticChildren: WidgetField = "getStaticChildren"
    getTargetPriority: WidgetField = "getTargetPriority"
    getTargetVerb: WidgetField = "getTargetVerb"
    getText: WidgetField = "getText"
    getTextColor: WidgetField = "getTextColor"
    getTextShadowed: WidgetField = "getTextShadowed"
    getType: WidgetField = "getType"
    getVarTransmitTrigger: WidgetField = "getVarTransmitTrigger"
    getWidth: WidgetField = "getWidth"
    getWidthMode: WidgetField = "getWidthMode"
    getXPositionMode: WidgetField = "getXPositionMode"
    getXTextAlignment: WidgetField = "getXTextAlignment"
    getYPositionMode: WidgetField = "getYPositionMode"
    getYTextAlignment: WidgetField = "getYTextAlignment"
    hasListener: WidgetField = "hasListener"


# Singleton instance for autocomplete
WidgetFields = _WidgetFields()


# --- Widget mask builder -------------------------------------------------


class Widget:
    """
    A Python-side mask builder for widget property queries.

    Usage with autocomplete:
        w = Widget(widget_id)
        w.enable(WidgetFields.getBounds)    # IDE autocomplete!
        w.enable(WidgetFields.getActions)
        data = w.get()

    Usage with strings (also valid):
        w = Widget(widget_id)
        w.enable("getBounds")
        w.enable("getActions")
        data = w.get()
    """

    _FIELDS: list[WidgetField] = list(typing.get_args(WidgetField))  # keeps exact order
    _FIELD_BITS = {name: 1 << i for i, name in enumerate(_FIELDS)}

    def __init__(self, id):
        self._mask = 0
        self.id = id

    # ---- Public API -----------------------------------------------------

    @property
    def mask(self) -> int:
        """Return the combined Java bitmask."""
        return self._mask

    def enable(self, field: WidgetField) -> "Widget":
        """Enable a specific getter flag."""
        self._mask |= self._FIELD_BITS[field]
        return self

    def disable(self, field: WidgetField) -> "Widget":
        """Disable a specific getter flag."""
        self._mask &= ~self._FIELD_BITS[field]
        return self

    def clear(self) -> "Widget":
        """Reset to 0."""
        self._mask = 0
        return self

    def enableAll(self) -> "Widget":
        """Enable all fields."""
        self._mask = (1 << len(self._FIELDS)) - 1
        return self

    # ---- Alternate constructors ----------------------------------------

    @classmethod
    def fromNames(cls, *fields: WidgetField) -> "Widget":
        """Build a mask in one line."""
        w = cls()
        for f in fields:
            w.enable(f)
        return w

    # ---- Debug helpers --------------------------------------------------

    def asDict(self) -> dict[str, bool]:
        """Return {field: enabled?}."""
        return {name: bool(self._mask & bit) for name, bit in self._FIELD_BITS.items()}

    def get(self) -> dict[str, typing.Any]:
        client = getClient()
        result = client.api.invokeCustomMethod(
            target="WidgetInspector",
            method="getWidgetProperties",
            signature="(IJ)[B",
            args=[self.id, self.mask],
            async_exec=self.getAsyncMode(),
        )

        return result

    def getChild(self, child_index: int) -> dict[str, typing.Any]:
        client = getClient()
        result = client.api.invokeCustomMethod(
            target="WidgetInspector",
            method="getWidgetChild",
            signature="(IIJ)[B",
            args=[self.id, child_index, self.mask],
            async_exec=self.getAsyncMode(),
        )

        return result

    def getChildren(self) -> list[dict[str, typing.Any]]:
        client = getClient()
        result = client.api.invokeCustomMethod(
            target="WidgetInspector",
            method="getWidgetChildren",
            signature="(IJ)[B",
            args=[self.id, self.mask],
            async_exec=self.getAsyncMode(),
        )

        return result

    def getChildrenMasked(self, childmask: list[int]) -> list[dict[str, typing.Any]]:
        client = getClient()
        result = client.api.invokeCustomMethod(
            target="WidgetInspector",
            method="getWidgetChildrenMasked",
            signature="(I[IJ)[B",
            args=[self.id, childmask, self.mask],
            async_exec=self.getAsyncMode(),
        )

        return result

    def getAsyncMode(self) -> bool:
        """
        Determine if async execution is safe for this widget query.

        Returns False if getParent or getParentId are in the mask, as these
        require synchronous execution to properly resolve parent references.

        Returns:
            True if async execution is safe, False otherwise
        """
        parent_fields = self._FIELD_BITS["getParent"] | self._FIELD_BITS["getParentId"]
        return (self._mask & parent_fields) == 0
