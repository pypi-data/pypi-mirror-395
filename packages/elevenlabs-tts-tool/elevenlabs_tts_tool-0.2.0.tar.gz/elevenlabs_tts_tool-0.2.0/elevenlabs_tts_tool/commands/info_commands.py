"""
Subscription info command implementation.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys
from datetime import datetime

import click

from elevenlabs_tts_tool.core.client import get_client
from elevenlabs_tts_tool.logging_config import get_logger

logger = get_logger(__name__)


@click.command()
@click.option(
    "--days",
    "-d",
    default=7,
    type=int,
    help="Number of days of historical usage to display (default: 7)",
)
def info(days: int) -> None:
    """
    Display ElevenLabs subscription and usage information.

    Shows current subscription status, character quota, usage statistics,
    and historical usage metrics for the specified time period.

    \b
    Examples:

    \b
        # View subscription info with last 7 days of usage
        elevenlabs-tty-tool info

    \b
        # View last 30 days of usage
        elevenlabs-tty-tool info --days 30

    \b
        # Quick quota check
        elevenlabs-tty-tool info --days 1

    \b
    Output Information:
        - Subscription tier and status
        - Character usage (used/limit/remaining)
        - Quota reset date
        - Historical usage breakdown by day
        - Total usage for the period
    """
    try:
        logger.info("Fetching subscription and usage information")
        logger.debug(f"Historical usage period: {days} days")

        # Initialize client
        logger.debug("Initializing ElevenLabs client")
        client = get_client()

        # Get subscription information
        click.echo("\nFetching subscription information...")
        logger.debug("Calling API: client.user.subscription.get()")
        subscription = client.user.subscription.get()
        logger.debug(f"Subscription tier: {subscription.tier}")
        logger.debug(f"Subscription status: {subscription.status}")

        # Display subscription info
        click.echo("\n" + "=" * 80)
        click.echo("ElevenLabs Subscription Information")
        click.echo("=" * 80)
        click.echo()

        # Basic subscription details
        click.echo(f"Tier:           {subscription.tier}")
        click.echo(f"Status:         {subscription.status}")

        # Character usage
        used = subscription.character_count
        limit = subscription.character_limit
        remaining = limit - used
        percentage = (used / limit * 100) if limit > 0 else 0

        click.echo()
        click.echo("Character Usage:")
        click.echo(f"  Used:         {used:,} characters")
        click.echo(f"  Limit:        {limit:,} characters")
        click.echo(f"  Remaining:    {remaining:,} characters")
        click.echo(f"  Percentage:   {percentage:.1f}%")

        # Usage bar visualization
        bar_width = 40
        filled = int(bar_width * used / limit) if limit > 0 else 0
        bar = "█" * filled + "░" * (bar_width - filled)
        click.echo(f"  [{bar}]")

        # Quota reset
        if subscription.next_character_count_reset_unix:
            reset_timestamp = subscription.next_character_count_reset_unix
            reset_date = datetime.fromtimestamp(reset_timestamp)
            click.echo()
            click.echo(f"Quota Resets:   {reset_date.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            click.echo(f"                ({reset_date.strftime('%A, %B %d, %Y')})")

        # Additional subscription details
        if hasattr(subscription, "voice_limit"):
            click.echo()
            click.echo(f"Voice Slots:    {subscription.voice_limit}")

        if hasattr(subscription, "currency"):
            click.echo(f"Currency:       {subscription.currency.upper()}")

        # Historical usage
        click.echo()
        click.echo("=" * 80)
        click.echo(f"Historical Usage (Last {days} Days)")
        click.echo("=" * 80)
        click.echo()

        try:
            # Calculate time range
            import time

            end_time = int(time.time() * 1000)  # Current time in milliseconds
            start_time = end_time - (days * 24 * 60 * 60 * 1000)  # N days ago

            # Get usage metrics
            usage = client.usage.get(
                start_unix=start_time, end_unix=end_time, aggregation_interval="day"
            )

            if usage.time and usage.usage:
                # Display usage by day
                total_usage = 0

                # Get the first usage category (usually the total)
                usage_category = list(usage.usage.keys())[0] if usage.usage else None

                if usage_category:
                    usage_values = usage.usage[usage_category]

                    click.echo(f"{'Date':<15} {'Characters Used':<20} {'Bar'}")
                    click.echo("-" * 80)

                    for timestamp, chars_used in zip(usage.time, usage_values):
                        # Convert timestamp to date
                        date = datetime.fromtimestamp(timestamp / 1000)
                        date_str = date.strftime("%Y-%m-%d")

                        # Calculate bar
                        chars_int = int(chars_used)
                        total_usage += chars_int

                        # Create mini bar (max 30 chars wide)
                        max_daily = max(usage_values) if usage_values else 1
                        bar_length = int(30 * chars_used / max_daily) if max_daily > 0 else 0
                        mini_bar = "█" * bar_length

                        click.echo(f"{date_str:<15} {chars_int:>10,} chars    {mini_bar}")

                    click.echo("-" * 80)
                    click.echo(f"{'Total:':<15} {total_usage:>10,} chars")
                    click.echo()

                    # Average daily usage
                    avg_daily = total_usage / len(usage_values) if usage_values else 0
                    click.echo(f"Average daily usage: {int(avg_daily):,} characters")

                    # Projected monthly usage
                    projected_monthly = avg_daily * 30
                    click.echo(f"Projected monthly:   {int(projected_monthly):,} characters")

                else:
                    click.echo("No usage data available for this period.")
            else:
                click.echo("No historical usage data available.")

        except Exception as e:
            click.echo(f"Warning: Could not fetch historical usage: {e}", err=True)

        click.echo()
        click.echo("=" * 80)
        click.echo()

        # Warnings if quota is running low
        if percentage >= 90:
            click.echo("⚠️  WARNING: You have used more than 90% of your quota!", err=True)
            reset_str = reset_date.strftime("%Y-%m-%d")
            click.echo(f"   Consider upgrading your plan or waiting until {reset_str}", err=True)
            click.echo()
        elif percentage >= 75:
            click.echo("ℹ️  NOTE: You have used more than 75% of your quota.")
            click.echo()

    except Exception as e:
        error_str = str(e)

        # Check for 401 missing_permissions error (free tier)
        if "status_code: 401" in error_str and "missing_permissions" in error_str:
            click.echo("\n" + "=" * 80, err=True)
            click.echo("⚠️  WARNING: API Key Permission Error (Status Code: 401)", err=True)
            click.echo("=" * 80, err=True)
            click.echo(err=True)
            click.echo("The API key you are using is missing the 'user_read' permission.", err=True)
            click.echo(
                "This operation is not available on the Free tier with default API keys.",
                err=True,
            )
            click.echo(err=True)
            click.echo("Troubleshooting:", err=True)
            click.echo(
                "  1. ⚠️  You are using the Free tier - subscription info is not available",
                err=True,
            )
            click.echo(
                "  2. Consider upgrading to a paid tier for API access to usage metrics",
                err=True,
            )
            click.echo("  3. Visit https://elevenlabs.io/pricing to view available tiers", err=True)
            click.echo(
                "  4. Verify your API key at https://elevenlabs.io/app/settings/api-keys",
                err=True,
            )
            click.echo(err=True)
            click.echo("=" * 80, err=True)
        else:
            # Generic error handling for other issues
            click.echo(f"Error: Failed to fetch subscription information: {e}", err=True)
            click.echo(
                "\nTroubleshooting:\n"
                "  1. Verify your ELEVENLABS_API_KEY is set correctly\n"
                "  2. Check your internet connection\n"
                "  3. Ensure your API key has the necessary permissions\n"
                "  4. Visit https://elevenlabs.io/app/settings/api-keys to verify your key",
                err=True,
            )

        sys.exit(1)
