from __future__ import annotations
import collections.abc
import datetime
import typing
from warnings import deprecated # type: ignore

import jpype # type: ignore
import jpype.protocol # type: ignore

import ghidra.app.plugin.core.debug.gui
import ghidra.framework.plugintool
import java.lang # type: ignore
import javax.swing # type: ignore


class DebuggerMethodInvocationDialog(ghidra.app.plugin.core.debug.gui.AbstractDebuggerParameterDialog[ghidra.trace.model.target.iface.TraceMethod.ParameterDescription[typing.Any]]):

    class_: typing.ClassVar[java.lang.Class]

    def __init__(self, tool: ghidra.framework.plugintool.PluginTool, title: typing.Union[java.lang.String, str], buttonText: typing.Union[java.lang.String, str], buttonIcon: javax.swing.Icon):
        ...



__all__ = ["DebuggerMethodInvocationDialog"]
