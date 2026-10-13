// HeadshotStudio.Tray — Windows tray shell that launches the Python CLI.
using System;
using System.Diagnostics;
using System.Windows.Forms;

namespace HeadshotStudio.Tray;

internal static class Program
{
    [STAThread]
    private static void Main()
    {
        ApplicationConfiguration.Initialize();
        var menu = new ContextMenuStrip();
        menu.Items.Add("Generate headshots\u2026", null, (_, _) => Launch("generate"));
        menu.Items.Add("Open outputs folder", null, (_, _) => Launch("open-outputs"));
        menu.Items.Add("Quit", null, (_, _) => Application.Exit());

        var icon = new NotifyIcon
        {
            Icon = SystemIcons.Application,
            Text = "AI Headshot Studio",
            Visible = true,
            ContextMenuStrip = menu,
        };
        Application.Run();
        icon.Dispose();
    }

    private static void Launch(string verb)
    {
        var psi = new ProcessStartInfo
        {
            FileName = "headshot-studio",
            Arguments = verb == "open-outputs" ? "styles" : "generate --style corporate_neutral",
            UseShellExecute = true,
        };
        Process.Start(psi);
    }
}