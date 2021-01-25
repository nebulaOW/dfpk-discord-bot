async def submitpb(ctx, map_code, level, record):
    # sanitize for injection
    sanitize(map_code)
    sanitize(record)
    sanitize(level)
    
    #input validation
    if not level.isnumeric() or int(level) not in range(0, 41):
        await ctx.channel.send("Level must be a number between 0 and 40")
        return
    if not isEnglish(map_code):
        await ctx.channel.send("Only letters A-Z and numbers 0-9 allowed.")
        return
    try:
        record = float(record)
    except:
        await ctx.channel.send("Please format record in seconds. ex: 00.00")
        return
    map_code = map_code.upper()

    # main
    if (
        WorldRecords.count_documents(
            {
                "map_code": map_code,
                "name": ctx.author.name,
                "level": level,
                "posted_by": ctx.author.id,
            }
        )
        == 0
    ):

        newSubmission = {
            "map_code": map_code,
            "name": ctx.author.name,
            "record": record,
            "level": level,
            "posted_by": ctx.author.id,
            "message_id": ctx.message.id,
        }
        WorldRecords.insert_one(newSubmission)
        await ctx.channel.send(
            (f"Personal best submission accepted:\n{map_code} level {level} - {ctx.author.name} - {record}")  # noqa: E501
        )

    elif (
        WorldRecords.count_documents(
            {
                "map_code": map_code,
                "name": ctx.author.name,
                "level": level,
                "posted_by": ctx.author.id,
            }
        )
        == 1
    ):
        search = WorldRecords.find_one(
            {
                "map_code": map_code,
                "name": ctx.author.name,
                "level": level,
                "posted_by": ctx.author.id,
            }
        )
        # convert strings into datetime obj to compare
        try:
            new_record = date_func(record)

            searched_record = date_func(search["record"])

            if new_record < searched_record:

                # store normal string, not datetime obj.
                WorldRecords.update_one(
                    search,
                    {
                        "$set": {
                            "record": record,
                            "level": level,
                            "message_id": ctx.message.id,
                        }
                    },
                )
                await ctx.channel.send(
                    ("Personal best update accepted:\n"
                        f"{map_code} level {level} - "
                        f"{ctx.author.name} - {record}")
                )
            else:

                await ctx.channel.send(
                    "Personal best needs to be faster to update."
                )
        except ValueError:
            await ctx.channel.send(
                ("Format the time correctly. 00:00:00.00 - Consider using the _/convertseconds <seconds>_ command.")  # noqa: E501
            )
