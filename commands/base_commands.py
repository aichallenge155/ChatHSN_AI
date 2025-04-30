import discord
from discord.ext import commands
from database import add_user, update_last_interaction, log_interaction
from ai import generate_response
from ai_styles import get_available_styles, get_style_description  
from utils import format_error_message
import random
from googletrans import Translator

translator = Translator()

# İngilis dilində olan əsas challenge-lər
base_challenges = [
    "📖 Read 5 pages of any book!",
    "🧠 Learn 3 new words in a foreign language!",
    "📝 Write down 2 goals for this week!",
    "💪 Do 20 push-ups!",
    "🧘‍♂️ Meditate for 10 minutes!",
    "🥤 Drink 2 liters of water today!",
    "🧹 Clean your workspace!",
    "🎯 Focus on one task for 30 minutes without distractions!",
    "👨‍💻 Solve 2 programming problems!",
    "✍️ Write a short paragraph about your day!",
    "🚶‍♂️ Walk at least 3000 steps!",
    "🛏️ Go to bed 30 minutes earlier tonight!",
    "🍎 Eat one healthy meal today!",
    "📚 Watch an educational video (at least 10 minutes long)!",
    "🔋 Take a 15-minute power nap!"
]

# Dil kodlarına uyğun bayraqlar və tam adlar
language_info = {
    "az": {"flag": "🇦🇿", "name": "Azərbaycan dili", "button_text": "✅ Tamamlandı!", "prompt_text": "Çağırışı tamamladıqdan sonra düyməni basın:"},
    "en": {"flag": "🇬🇧", "name": "English", "button_text": "✅ Completed!", "prompt_text": "Press the button after completing your challenge:"},
    "ru": {"flag": "🇷🇺", "name": "Русский", "button_text": "✅ Выполнено!", "prompt_text": "Нажмите на кнопку после завершения задания:"},
    "tr": {"flag": "🇹🇷", "name": "Türkçe", "button_text": "✅ Tamamlandı!", "prompt_text": "Görevi tamamladıktan sonra butona basın:"},
    "fr": {"flag": "🇫🇷", "name": "Français", "button_text": "✅ Terminé!", "prompt_text": "Appuyez sur le bouton après avoir terminé votre défi:"},
    "de": {"flag": "🇩🇪", "name": "Deutsch", "button_text": "✅ Erledigt!", "prompt_text": "Drücken Sie den Knopf, nachdem Sie Ihre Herausforderung abgeschlossen haben:"},
    "es": {"flag": "🇪🇸", "name": "Español", "button_text": "✅ Completado!", "prompt_text": "Presiona el botón después de completar tu desafío:"}
}

# Mətnin dilini aşkarlamaq üçün funksiya
def detect_language(text):
    try:
        detected = translator.detect(text)
        return detected.lang
    except:
        return "en"  # Default olaraq İngilis dili qaytarılır

# Mətni tərcümə etmək üçün funksiya
def translate_text(text, target_lang):
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Xəta baş verərsə, orijinal mətni qaytarır

# Yardım komandalarını ehtiva edən boş sinif (istəyə görə genişləndirilə bilər)
class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

class CompleteButton(discord.ui.View):
    def __init__(self, language_code):
        super().__init__(timeout=900)
        self.language_code = language_code
        button_text = language_info.get(language_code, language_info["en"])["button_text"]
        
        # Düymənin mətnini dəyişirik
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.label = button_text

    @discord.ui.button(label="✅ Completed!", style=discord.ButtonStyle.success)
    async def complete(self, interaction: discord.Interaction, button: discord.ui.Button):
        success_message = "Challenge completed! Congratulations! 🎉"
        if self.language_code != "en":
            success_message = translate_text(success_message, self.language_code)
        
        await interaction.response.send_message(success_message, ephemeral=True)
        
        # Düyməni söndürürük və mesajı yeniləyirik (düyməsiz)
        self.stop()
        await interaction.message.edit(view=None)

# Botun əsas komandalarını toplayan sinif
class BaseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_style = "default"
        self.user_styles = {}  # İstifadəçi ID-yə görə üslub seçimi saxlanır

    # Bot tam olaraq Discord serverlərinə qoşulduqda işləyir
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is connected to Discord!")
        print(f"Connected to {len(self.bot.guilds)} servers")
    
    # Hər mesaj yazıldıqda işləyən funksiyadır
    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't respond to our own messages
        if message.author == self.bot.user:
            return
        
        # İstifadəçi bot deyilsə, onu verilənlər bazasına əlavə et və vaxtını yenilə
        if not message.author.bot:
            add_user(str(message.author.id), message.author.name)
            update_last_interaction(str(message.author.id))
    
    # !ask komandı — istifadəçi sual verir və AI cavab yaradır
    @commands.command(name="ask")
    async def ask(self, ctx, *, prompt=None):
        """Ask the AI a question or provide a prompt."""
        if not prompt:
            await ctx.send(format_error_message("empty_prompt"))
            return
        
        # İstifadəçi məlumatlarını logla
        try:
            add_user(str(ctx.author.id), ctx.author.name)
            update_last_interaction(str(ctx.author.id))
            log_interaction(str(ctx.author.id), prompt)
        except Exception as e:
            await ctx.send(format_error_message("api_error"))
            print(f"Error logging interaction: {e}")
            return
        
        # Get the user's preferred style or use the default
        style = self.user_styles.get(str(ctx.author.id), self.default_style)
        
        # Show typing indicator
        async with ctx.typing():
            # Generate AI response
            try:
                response = await generate_response(prompt, style) # AI cavabı al
                await ctx.send(response)  # Cavabı göndər
            except Exception as e:
                await ctx.send(format_error_message("api_error"))
                print(f"Error generating response: {e}")
    
    # İstifadəçinin seçdiyi üslubu al
    @commands.command(name="style")
    async def set_style(self, ctx, style_name=None):
        """Set your preferred response style."""
        if not style_name:
            # List available styles
            styles = get_available_styles()
            current_style = self.user_styles.get(str(ctx.author.id), self.default_style)
            
            embed = discord.Embed(
                title="Available Response Styles",
                description=f"Your current style: **{current_style}**\n\nUse `!style [name]` to change your style.",
                color=discord.Color.blue()
            )
            
            for style in styles:
                embed.add_field(
                    name=style.capitalize(),
                    value=get_style_description(style)[:100] + "...",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            return
        
        # Əgər stil adı mövcud deyilsə, xəta göndər
        available_styles = get_available_styles()
        if style_name.lower() not in available_styles:
            await ctx.send(format_error_message("style_not_found"))
            return
        
        # Set the user's preferred style
        self.user_styles[str(ctx.author.id)] = style_name.lower()
        
        # Confirm the style change
        await ctx.send(f"Your response style has been set to **{style_name.lower()}**.")
    
    @commands.command(name="challenge")
    async def challenge(self, ctx, language_code=None):
        """Get a random daily challenge in the specified language. Usage: !challenge [language_code]"""
        # Əgər dil kodu verilməyibsə, mesajın özünün dilini aşkarlayırıq
        message_content = ctx.message.content.replace("!challenge", "").strip()
        
        if language_code is None or language_code not in language_info:
            if message_content:
                # Mesajın dilini aşkarlayırıq
                detected_lang = detect_language(message_content)
                language_code = detected_lang if detected_lang in language_info else "en"
            else:
                # Default olaraq İngilis dili seçirik
                language_code = "en"
        
        # Təsadüfi bir challenge seçirik
        selected_challenge = random.choice(base_challenges)
        
        # Challenge-i lazım gələrsə tərcümə edirik
        if language_code != "en":
            translated_challenge = translate_text(selected_challenge, language_code)
        else:
            translated_challenge = selected_challenge
        
        # Dilə uyğun məlumatı alırıq
        lang_data = language_info.get(language_code, language_info["en"])
        lang_name = f"{lang_data['name']} {lang_data['flag']}"
        prompt_text = lang_data["prompt_text"]
        
        embed = discord.Embed(
            title="🌟 Daily Challenge 🌟",
            description=(
                f"**{lang_name}**\n\n"
                f"> {translated_challenge}\n\n"
                f"{prompt_text}"
            ),
            color=discord.Color.purple()
        )
        
        # Footer-i tərcümə edirik
        footer_text = "Complete challenges and grow every day! 🚀"
        if language_code != "en":
            footer_text = translate_text(footer_text, language_code)
        
        embed.set_footer(text=footer_text)
        
        # Dilə uyğun düyməni yaradırıq
        button_view = CompleteButton(language_code)
        await ctx.send(embed=embed, view=button_view)

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Show help information about the bot."""
        embed = discord.Embed(
            title="🤖 AI Assistant Bot Help",
            description="I'm your AI assistant here to make life easier! Here's what I can do:",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="📌 Basic Commands",
            value=(
                "**`!ask [prompt]`** - Ask anything or get AI-generated answers\n"
                "**`!style`** - View and customize your response style\n"
                "**`!help`** - Display this help message\n"
                "**`!challenge [language_code]`** - Start a challenge in specified language (e.g. en, az, ru, tr, fr, de, es)"
            ),
            inline=False
        )

        embed.add_field(
            name="🧠 Special Commands",
            value=(
                "**`!cite [topic]`** - Get a trusted citation on any topic\n"
                "**`!define [term]`** - Define any word or concept\n"
                "**`!studyplan [topic]`** - Generate a personalized study plan\n"
                "**`!image [description]`** - Create a picture based on the description\n"
                "**`!convert [from_format] [to_format]`** - Convert an uploaded file into the desired format (e.g., PDF ➔ DOCX)\n"
                "**`!analyse [file]`** - Upload a file for analysis, text extraction, or format detection."
            ),
            inline=False
        )

        embed.set_footer(text="Type a command to get started! If you're stuck, just ask for help.")

        await ctx.send(embed=embed)   # Kömək mesajını göndər
   
# Bot üçün bu modulun yüklənməsi
async def setup(bot):
    await bot.add_cog(BaseCommands(bot))  # BaseCommands sinfini bota əlavə et