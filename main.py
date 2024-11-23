import os
import requests

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_friends(user_id):
    url = f"https://friends.roblox.com/v1/users/{user_id}/friends"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        friends_data = response.json()
        if 'data' in friends_data:
            return friends_data['data']
        else:
            print("\nError: User ID not found or has no friends.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching friends: {e}")
        return None
    except ValueError:
        print("Error: Unable to decode JSON.")
        return None

def fetch_user_details(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        user_data = response.json()
        if user_data.get("id") is None:
            print(f"\nError: User ID {user_id} does not exist.")
            return None
        return user_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user details: {e}")
        return None

def save_to_file(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)
        print(f"\nData successfully saved to {filename}.")
    except Exception as e:
        print(f"\nError saving to file: {e}")

def main():
    while True:
        try:
            user_id = input("Enter the Roblox User ID (or type 'exit' to quit): ").strip()
            if user_id.lower() == 'exit':
                print("Exiting the tool. Goodbye!")
                break
            user_id = int(user_id)
            user_details = fetch_user_details(user_id)
            if user_details is None:
                print("\nUser does not exist. Please try again with a valid ID.")
                input("\nPress Enter to continue...")
                clear_console()
                continue
            user_name = user_details.get('name', 'N/A')
            user_display_name = user_details.get('displayName', 'N/A')
            friends = get_friends(user_id)
            output_data = []
            if friends is not None:
                if len(friends) > 0:
                    header = f"Friends of User ID {user_id} ({user_name} - {user_display_name}):"
                    print(f"\n{header}\n")
                    print(f"{'ID':<15}{'Name':<20}{'Display Name':<20}")
                    print("-" * 55)
                    output_data.append(header)
                    output_data.append(f"{'ID':<15}{'Name':<20}{'Display Name':<20}")
                    output_data.append("-" * 55)
                    for friend in friends:
                        friend_id = friend.get('id')
                        friend_details = fetch_user_details(friend_id)
                        if friend_details:
                            name = friend_details.get('name', 'N/A')
                            display_name = friend_details.get('displayName', 'N/A')
                            print(f"{friend_id:<15}{name:<20}{display_name:<20}")
                            output_data.append(f"{friend_id:<15}{name:<20}{display_name:<20}")
                        else:
                            print(f"{friend_id:<15}{'Error fetching':<20}{'details':<20}")
                            output_data.append(f"{friend_id:<15}{'Error fetching':<20}{'details':<20}")
                    print(f"\nTotal friends: {len(friends)}")
                    output_data.append(f"\nTotal friends: {len(friends)}")
                else:
                    print(f"\nUser ID {user_id} ({user_name} - {user_display_name}) has no friends.")
                    output_data.append(f"\nUser ID {user_id} ({user_name} - {user_display_name}) has no friends.")
            else:
                print("\nFailed to retrieve friends or the user does not exist.")
                output_data.append("\nFailed to retrieve friends or the user does not exist.")
            save_choice = input("\nDo you want to save this information to a file? (yes/no): ").strip().lower()
            if save_choice in ['yes', 'y']:
                filename = input("Enter the filename (e.g., friends_info.txt): ").strip()
                save_to_file(filename, "\n".join(output_data))
        except ValueError:
            print("\nInvalid User ID. Please enter a numeric ID.")
        input("\nPress Enter to continue...")
        clear_console()

if __name__ == "__main__":
    main()
