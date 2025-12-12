import click
import subprocess
from pathlib import Path
import random

from .action_modules import _login, _signin, _signout

@click.group()
def main():
    """
    Automate UKG Dimensions actions with Okta.
    """
    pass

@main.command()
def install_browsers():
    """
    Install Playwright browser binaries.
    """
    click.echo("Installing Playwright browsers...")
    subprocess.run(["playwright", "install"], check=True)

@main.command()
def install_cron():
    """
    Add cron job for resetting signin/signout time every day
    """
    python_path = subprocess.check_output(["which", "python3"]).decode().strip()
    reset_cmd = f"{python_path} auto_ukg reset-cron"
    log_file = Path.home() / ".auto_ukg.log"

    # reset cron jobs at midnight every night
    cron_entry = f"0 0 * * 1-5 {reset_cmd} >> {log_file} 2>&1\n" 

    # Read existing crontab
    existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    current_cron = existing.stdout if existing.returncode == 0 else ""

    if "auto_ukg reset_cron" in current_cron:
        click.echo("Cron jobs already installed.")
        return
    
    new_cron = current_cron + "\n" + cron_entry

    # Install new crontab
    p = subprocess.Popen(["crontab"], stdin=subprocess.PIPE, text=True)
    p.communicate(new_cron)

    click.echo("Cron jobs installed:")
    click.echo(cron_entry)

@main.command()
def reset_cron():
    """
    Add cron jobs for 8:30 AM and 5:00 PM on weekdays, +/- a few minutes
    """
    
    python_path = subprocess.check_output(["which", "python3"]).decode().strip()
    signin_cmd = f"{python_path} auto_ukg signin"
    signout_cmd = f"{python_path} auto_ukg signout"
    log_file = Path.home() / ".auto_ukg.log"

    offset = random.randint(-29, 29)

    cron_entry = (
        f"{30+offset} 8 * * 1-5 {signin_cmd} >> {log_file} 2>&1\n"
        f"{(0+offset)%60} {17 if offset >= 0 else 16} * * 1-5 {signout_cmd} >> {log_file} 2>&1\n"
    )

    # Read existing crontab
    existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    current_cron = existing.stdout if existing.returncode == 0 else ""

    # Delete existing signin/out entries
    if "auto_ukg signin" in current_cron and "auto_ukg signout" in current_cron:

        crontab_output = subprocess.Popen(["crontab", "-l"], stdout=subprocess.PIPE)
        non_signin = subprocess.Popen(["grep", "-v", "'auto_ukg signin'"], stdin=crontab_output.stdout, stdout=subprocess.PIPE)
        non_signin_signout = subprocess.Popen(["grep", "-v", "'auto_ukg signout'"], stdin=non_signin.stdout, stdout=subprocess.DEVNULL)
        p = subprocess.Popen(["crontab"], stdin=subprocess.PIPE, text=True)
        p.communicate(non_signin_signout.stdout)

    # Read existing crontab
    existing = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    current_cron = existing.stdout if existing.returncode == 0 else ""

    new_cron = current_cron + "\n" + cron_entry

    # Install new crontab
    p = subprocess.Popen(["crontab"], stdin=subprocess.PIPE, text=True)
    p.communicate(new_cron)

    click.echo("Cron jobs installed:")
    click.echo(cron_entry)

@main.command()
def login():
    """
    Perform initial Okta login (manual)
    """
    _login()

@main.command()
def signin():
    """
    Automatically clock in
    """
    try:
        _signin()
    except:
        _login()

@main.command()
def signout():
    """
    Automatically clock out
    """
    try:
        _signout()
    except:
        _login()

if __name__ == '__main__':
    main()