# Debugging

You can always use  `pdb` and set `breakpoint()` anywhere.

If you are using an editor with build in debugger you need to set our script as an entry point. 
However, you often can't simply set it to `ai-parade` as it is necessary to set it to the underlying python entrypoint.
Which in our case it is installed at `.venv/lib/python3.13/site-packages/ai_parade/_cli/ai_parade/main.py` (replace python version with yours).

Here are a few snippets you can use.

## VSCode

> [!WARNING]
> Don't use `--separate-environment`. The separate environment can't be debugged even with `"subProcess": true,`

Example of `launch.json`

```json
{
	"version": "0.2.0",
	"configurations": [
		{
			"name": "ai-parade",
			"type": "debugpy",
			"request": "launch",
			"program": ".venv/lib/python3.13/site-packages/ai_parade/_cli/ai_parade/main.py",
			"args": "${command:pickArgs}",
			"console": "integratedTerminal",
			// Problem in our code? uncomment this:
			//"justMyCode": false,
			
			// Or this:
			//"rules": [
			//	{
			//		"path": "**/ai_parade/**/*",
			//		"include": true
			//	}
			//]
			// see "docs": https://github.com/microsoft/debugpy/issues/561#issuecomment-797735593
		}
	]
}
```
