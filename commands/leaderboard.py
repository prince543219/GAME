from sqlalchemy import create_engine, Table, Column, Integer, MetaData, select, DateTime
from datetime import datetime, timedelta

# Define the database connection (update with your database details)
DATABASE_URL = "sqlite:///bot_database.db"  # Replace with your database URL if different
db_engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the scores table (ensure it matches your database schema)
scores_table = Table(
    "scores",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("chat_id", Integer, nullable=False),
    Column("score", Integer, default=0),
    Column("timestamp", DateTime, default=datetime.utcnow)
)

# Create the table if it doesn't exist
metadata.create_all(db_engine)

# Command name
command = "leaderboard"

# Command handler function
async def handler(event):
    """Handle the /leaderboard command to display the top scores."""
    chat_id = event.chat_id
    now = datetime.utcnow()
    twenty_four_hours_ago = now - timedelta(hours=24)
    
    try:
        # Fetch leaderboard data from the database
        with db_engine.connect() as connection:
            stmt = (
                select(scores_table.c.user_id, scores_table.c.score)
                .where(scores_table.c.chat_id == chat_id)
                .where(scores_table.c.timestamp >= twenty_four_hours_ago)
                .order_by(scores_table.c.score.desc())
                .limit(10)
            )
            results = connection.execute(stmt).fetchall()

        # Check if there are scores to display
        if not results:
            await event.respond("No leaderboard data available yet! Start playing to be featured here.")
            return

        # Format leaderboard response
        leaderboard_text = "**🏆 Leaderboard (Last 24 Hours):**\n\n"
        for rank, (user_id, score) in enumerate(results, start=1):
            try:
                user = await event.client.get_entity(user_id)
                user_name = user.first_name or "Anonymous"
                leaderboard_text += f"{rank}. {user_name} - {score} points\n"
            except Exception as e:
                print(f"Error fetching user {user_id}: {e}")

        # Send the leaderboard response
        await event.respond(leaderboard_text)

    except Exception as e:
        print(f"Error in /leaderboard handler: {e}")
        await event.respond("An error occurred while fetching the leaderboard. Please try again later.")
