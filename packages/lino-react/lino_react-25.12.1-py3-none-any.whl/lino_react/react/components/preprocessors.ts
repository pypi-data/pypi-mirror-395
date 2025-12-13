
import * as t from "./types";

const Lino: t.Lino = window.Lino || {};

Lino.get_current_grid_config = (context, preprocessedStack) => {
    context.dataContext.root.get_current_grid_config(preprocessedStack);
    return preprocessedStack;
}

Lino.captureImage = (context, preprocessedStack) => {
    preprocessedStack.callback = {
        callback: (windowId) => {
            context.APP.dialogFactory.createWebcamDialog(context, preprocessedStack, windowId);
        },
        callbackType: "postWindowInit",
    }
    return preprocessedStack;
}

export { Lino };
