from pymongo import MongoClient
from datetime import datetime, timedelta

# Define the database connection (update with your database details)
client = MongoClient("mongodb+srv://surajit54321:surajit54321@cluster0.7mn37.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Replace with your MongoDB connection string
db = client["Cluster0"]

# Define the scores collection
scores_collection = db["scores"]

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
        results = scores_collection.find(
            {"chat_id": chat_id, "timestamp": {"$gte": twenty_four_hours_ago}}
        ).sort("score", -1).limit(10)

        # Check if there are scores to display
        if results.count() == 0:
            await event.respond("No leaderboard data available yet! Start playing to be featured here.")
            return

        # Format leaderboard response
        leaderboard_text = "**🏆 Leaderboard (Last 24 Hours):**\n\n"
        for rank, entry in enumerate(results, start=1):
            try:
                user = await event.client.get_entity(entry["user_id"])
                user_name = user.first_name or "Anonymous"
                leaderboard_text += f"{rank}. {user_name} - {entry['score']} points\n"
            except Exception as e:
                print(f"Error fetching user {entry['user_id']}: {e}")

        # Send the leaderboard response
        await event.respond(leaderboard_text)

    except Exception as e:
        print(f"Error in /leaderboard handler: {e}")
        await event.respond("An error occurred while fetching the leaderboard. Please try again later.")
