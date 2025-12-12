# VerSecBot

This is a relatively extendable bot that originated as a secretary for the Hades Speedrunning Discord server.

To add a task for VerSecBot to handle, you'll need to create a plugin. The task should define a `should_act` function, which accepts a message and returns a boolean of whether this task should be activated. It should also define an `act` function, which accepts a message and performs the action.

You'll need to use the versecbot-interface project as the base for your plugin.
