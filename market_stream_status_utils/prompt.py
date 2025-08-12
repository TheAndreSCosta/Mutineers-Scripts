def prompt_environment():
    while True:
        env = input("Select environment [dev/prd]: ").strip().lower()
        if env in ["dev", "prd"]:
            return env
        print("Invalid input. Please enter 'dev' or 'prd'.")


def prompt_dev_flavors():
    print("\nSelect dev flavor(s):")
    print("  1 - intbs1")
    print("  2 - nxtbs1")
    print("  3 - both (default)")
    choice = input("Enter choice [1/2/3]: ").strip()

    if choice == "1":
        return ["intbs1"]
    elif choice == "2":
        return ["nxtbs1"]
    else:
        return ["intbs1", "nxtbs1"]


def prompt_data_centers(env, env_dcs):
    dc_l = ", ".join(env_dcs)
    prompt = f"Enter comma-separated {env.upper()} DCs \n ({dc_l}) \n or press Enter to use all: "
    user_input = input(prompt).strip()
    if not user_input:
        return env_dcs
    selected_dcs = [dc.strip().lower() for dc in user_input.split(',') if dc.strip()]
    valid_dcs = [dc for dc in selected_dcs if dc in env_dcs]
    if not valid_dcs:
        print("No valid DCs entered.")
        return prompt_data_centers(env, env_dcs)
    return valid_dcs