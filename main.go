package main

import (
	"fmt"
	"runtime"
	"time"
)

// main initializes the appropriate shell executor based on the OS and executes a test command.
func main() {
	var executor ShellExecutor
	if runtime.GOOS == "windows" {
		executor = WindowsShellExecutor{}
	} else {
		executor = LinuxShellExecutor{}
	}

	//exitCode, stdout, stderr, err := executor.RunCommand([]string{"echo Hello, World!"}, 5*time.Second)
	powershellScript := `
Write-Host "Line 1";
Write-Host "Line 2";
Write-Host "Line 3";
exit 0;
`
	exitCode, stdout, stderr, err := executor.RunMultiLineCommand(powershellScript, 60*time.Second)
	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Exit Code:", exitCode)
		fmt.Println("Stdout:", stdout)
		fmt.Println("Stderr:", stderr)
	}
}
