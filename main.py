import discord
from discord.ext import commands
from pdf2image import convert_from_path

TOKEN = 'ADDTOKENHERE'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Bot is ready. Connected to {len(bot.guilds)} guilds.')

@bot.command()
async def send_pages(ctx, file_path):
    try:
        print(f'Sending pages for file: {file_path}')

        images = convert_from_path(file_path)
        total_pages = len(images)
        print(f'Total pages: {total_pages}')

        for page_number, image in enumerate(images):
            print(f'Sending page {page_number + 1}/{total_pages}')

            image_path = f'page_{page_number + 1}.png'
            image.save(image_path, 'PNG')

            embed = discord.Embed(title=f'Page {page_number + 1}', description=f'Page {page_number + 1}/{total_pages}')
            embed.set_image(url=f'attachment://{image_path}')

            with open(image_path, 'rb') as image_file:
                file = discord.File(image_file, filename=image_path)
                await ctx.send(embed=embed, file=file)

        print('All pages sent successfully.')

    except Exception as e:
        print(f'Error: {str(e)}')
        await ctx.send(f'Error: {str(e)}')

bot.run(TOKEN)
