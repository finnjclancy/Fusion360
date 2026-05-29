import importlib
import os
import traceback

import adsk.core

from ... import config
from ... import model_builder
from ...lib import fusionAddInUtils as futil


app = adsk.core.Application.get()
ui = app.userInterface

CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_rebuild_live_model'
CMD_NAME = 'Rebuild Live Model'
CMD_DESCRIPTION = 'Rebuild the active design from design_spec.json.'
IS_PROMOTED = True

WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

local_handlers = []


def start():
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    old_control = panel.controls.itemById(CMD_ID)
    if old_control:
        old_control.deleteMe()

    old_def = ui.commandDefinitions.itemById(CMD_ID)
    if old_def:
        old_def.deleteMe()

    cmd_def = ui.commandDefinitions.addButtonDefinition(
        CMD_ID,
        CMD_NAME,
        CMD_DESCRIPTION,
        ICON_FOLDER,
    )
    futil.add_handler(cmd_def.commandCreated, command_created)

    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)
    control.isPromoted = IS_PROMOTED


def stop():
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    if command_control:
        command_control.deleteMe()

    if command_definition:
        command_definition.deleteMe()


def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f'{CMD_NAME}: command created.')
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


def command_execute(args: adsk.core.CommandEventArgs):
    try:
        importlib.reload(model_builder)
        summary = model_builder.build_from_spec()
        ui.messageBox(summary, 'Fusion Live Model')
    except Exception:
        ui.messageBox(traceback.format_exc(), 'Fusion Live Model Error')


def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f'{CMD_NAME}: command destroyed.')
