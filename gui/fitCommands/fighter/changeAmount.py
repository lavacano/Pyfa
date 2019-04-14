import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calcCommands.fighter.changeAmount import CalcChangeFighterAmountCommand
from gui.fitCommands.calcCommands.fighter.localRemove import CalcRemoveLocalFighterCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeFighterAmountCommand(wx.Command):

    def __init__(self, fitID, position, amount):
        wx.Command.__init__(self, True, 'Change Fighter Amount')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.amount = amount

    def Do(self):
        if self.amount > 0:
            cmd = CalcChangeFighterAmountCommand(fitID=self.fitID, projected=False, position=self.position, amount=self.amount)
            if self.internalHistory.submit(cmd):
                Fit.getInstance().recalc(self.fitID)
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        else:
            cmd = CalcRemoveLocalFighterCommand(fitID=self.fitID, position=self.position)
            if self.internalHistory.submit(cmd):
                Fit.getInstance().recalc(self.fitID)
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
