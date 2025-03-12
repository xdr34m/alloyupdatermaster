package main

import (
	"bytes"
	"context"
	"fmt"
	"os/exec"
	"strings"
	"time"
)

type ShellExecutor interface {
	RunCommand(command []string, timeout time.Duration) (int, string, string, error)
	RunMultiLineCommand(command string, timeout time.Duration) (int, string, string, error)
}

// WindowsShellExecutor implements ShellExecutor for Windows PowerShell execution.
type WindowsShellExecutor struct{}

// LinuxShellExecutor implements ShellExecutor for Linux Bash execution.
type LinuxShellExecutor struct{}

// RunCommand executes a command in Windows PowerShell with a timeout.
// Returns exit code, stdout, stderr, and an error if applicable.
func (e WindowsShellExecutor) RunCommand(command []string, timeout time.Duration) (int, string, string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	commandStr := strings.Join(command, " ")
	cmd := exec.CommandContext(ctx, "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", commandStr)
	var stdoutBuf, stderrBuf bytes.Buffer
	cmd.Stdout = &stdoutBuf
	cmd.Stderr = &stderrBuf
	cmd.Stdin = nil
	err := cmd.Run()
	exitCode := 0
	if err != nil {
		if ctx.Err() == context.DeadlineExceeded {
			return -1, "", "", fmt.Errorf("command timed out")
		}
		if exitError, ok := err.(*exec.ExitError); ok {
			exitCode = exitError.ExitCode()
		} else {
			return -1, "", "", fmt.Errorf("failed to run command: %v", err)
		}
	}
	stdout, stderr := cleanOutput(stdoutBuf.String()), cleanOutput(stderrBuf.String())
	return exitCode, stdout, stderr, nil
}

// RunMultiLineCommand executes a multiline command in Windows PowerShell with a timeout.
// Returns exit code, stdout, stderr, and an error if applicable.
func (e WindowsShellExecutor) RunMultiLineCommand(str string, timeout time.Duration) (int, string, string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	cmd := exec.CommandContext(ctx, "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", fmt.Sprintf("& {%s}", str))
	var stdoutBuf, stderrBuf bytes.Buffer
	cmd.Stdout = &stdoutBuf
	cmd.Stderr = &stderrBuf
	cmd.Stdin = nil
	err := cmd.Run()
	exitCode := 0
	if err != nil {
		if ctx.Err() == context.DeadlineExceeded {
			return -1, "", "", fmt.Errorf("multiLineCommand timed out")
		}
		if exitError, ok := err.(*exec.ExitError); ok {
			exitCode = exitError.ExitCode()
		} else {
			return -1, "", "", fmt.Errorf("failed to run multiLineCommand: %v", err)
		}
	}
	stdout, stderr := cleanOutput(stdoutBuf.String()), cleanOutput(stderrBuf.String())
	return exitCode, stdout, stderr, nil
}

// RunCommand executes a command in Linux Bash with a timeout.
// Returns exit code, stdout, stderr, and an error if applicable.
func (e LinuxShellExecutor) RunCommand(command []string, timeout time.Duration) (int, string, string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	cmdArgs := append([]string{"-c"}, strings.Join(command, " "))
	cmd := exec.CommandContext(ctx, "bash", cmdArgs...)
	var stdoutBuf, stderrBuf bytes.Buffer
	cmd.Stdout = &stdoutBuf
	cmd.Stderr = &stderrBuf
	cmd.Stdin = nil
	err := cmd.Run()
	exitCode := 0
	if err != nil {
		if ctx.Err() == context.DeadlineExceeded {
			return -1, "", "", fmt.Errorf("command timed out")
		}
		if exitError, ok := err.(*exec.ExitError); ok {
			exitCode = exitError.ExitCode()
		} else {
			return -1, "", "", fmt.Errorf("failed to run command: %v", err)
		}
	}
	stdout, stderr := cleanOutput(stdoutBuf.String()), cleanOutput(stderrBuf.String())
	return exitCode, stdout, stderr, nil
}

// RunMultiLineCommand executes a multiline command in Linux Bash with a timeout.
// Returns exit code, stdout, stderr, and an error if applicable. Not implemented
func (e LinuxShellExecutor) RunMultiLineCommand(str string, timeout time.Duration) (int, string, string, error) {
	return -1, "", "", fmt.Errorf("multiLineCommand not implemented")
}
