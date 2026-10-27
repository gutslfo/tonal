# Where the voice file goes, read on 2026-10-26

Each line below was read on the platform's own help page on 26 October 2026, from Chiang Mai, signed out. The pages were saved as text during the build; the quotes are short excerpts. Limits move and whole features disappear: three of the five places the brief named on the same morning had changed (Custom GPTs closed to personal accounts, Claude Styles gone from the help centre, Gems retiring).

## ChatGPT

Source: [ChatGPT Custom Instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions), [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [Creating and editing GPTs](https://help.openai.com/en/articles/8554397-creating-a-gpt). help.openai.com refused WebFetch (403); read with curl.

- Custom instructions: "Custom instructions are available on all plans on Web, Desktop, iOS, and Android."
- Path, web and desktop: Settings, Personalization, "Enable customization" on, the Custom Instructions field. iOS and Android: Settings, Customize ChatGPT, same field.
- Limit: "Free and Go users can save up to 1,500 characters in custom instructions. Plus, Pro, Enterprise, Business, and Education users can save up to 5,000 characters." This is the limit the short file is built for.
- Projects: "Select the more options menu (•••), then select Project settings to add instructions for the project." "Project instructions apply only within that project and override your global custom instructions." No character limit is published for project instructions. Files per project: Free 5, Plus and Go 25, Pro 40.
- Custom GPTs: "New GPT creation and publishing are not available on personal ChatGPT accounts, including Free, Go, Plus, and Pro." "We're planning to retire custom GPTs." The brief's "Custom GPT, 8,000 characters" target is gone for a founder on a personal plan.

## Claude

Source: [Understanding Claude's personalization features](https://support.claude.com/en/articles/10185728), [What are projects?](https://support.claude.com/en/articles/9517075-what-are-projects), [How can I create and manage projects?](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects).

- The Styles article the brief linked (10185698) redirects to a 404. The personalization page no longer lists Styles. Not verified whether Styles survive inside the app for existing users; the kit does not send anyone there.
- Account-wide instructions: "Select "Settings," then "Your Claude" (or "Account" in the older Settings layout). Under "Instructions" ... Any instructions you add here will be applied to all of your conversations with Claude." No character limit is published.
- Projects: "Projects are available to all users, including those with free Claude accounts. Free users can create a maximum of five projects." Path: "Click on "Set project instructions."" then "Save instructions." A knowledge base sits on the right of the project page.
- One contradiction on the personalization page: "Use project instructions when you need specific guidance or context for a particular project (paid plans only)." Two other pages say projects are open to free accounts. The kit follows the two dedicated project pages and says free accounts can use projects.

## Gemini

Source: [Create & manage skills for Gemini Apps](https://support.google.com/gemini/answer/17094296), [Write effective skills](https://support.google.com/gemini/answer/17102773), [About the transition from Gems to skills](https://support.google.com/gemini/answer/18560919), [Save info and reference past chats](https://support.google.com/gemini/answer/16413516).

- Gems are ending: "Starting in November 2026, Gems will transition to skills in Gemini Apps for personal Google Accounts". "November 17, 2026: Gems transition to skills and become read only." The post goes out on 4 November, so the kit sends founders to skills, not Gems.
- Skills: "Skills are now available in Gemini chat to individuals over 18 signed in to a personal Google Account." Keep Activity has to be on.
- Path: on gemini.google.com, the sidebar, Customize (under More if hidden), Skills, Create, Create manually: "Enter the name of your skill, a description of what it does, and instructions for it to follow."
- Limits: the description is "within the 1024 character limit". No limit is published for the instructions. Reference files: "The total size of all uploaded files must not exceed 100 MB."
- Texts in a skill (read 27.10.2026): "You can add reference files to skills only by uploading them with your skill" (a SKILL.md file, or a folder or .zip with SKILL.md at its root; .docx not supported). A skill made by hand has a name, a description and instructions, no files. "Write effective skills": "Include structural templates or clear examples within your skill's instructions. This improves Gemini's accuracy, especially with formatting." So the guide has the founder paste the texts below the full file, under OUR TEXTS, the words the file already uses for them.
- What decides use: "Gemini only checks the skill's name and description to determine if a skill is relevant for your task." So the kit gives the founder a description that names every kind of text the brand writes, and says they can also name the skill in a chat.
- Personal context (Settings & help, Personal context, or gemini.google.com/saved-info): "You can save info about your life, work, or preferences". Not for under 18s. The examples on the page are one line long ("Always give me vegetarian recipes.") and no limit is published. The kit uses a skill instead, which is made for instructions of this length; Personal context is not tested here.

## Labels in French and Spanish

Read the same day on the localized help pages (help.openai.com/fr-fr and /es-es, support.claude.com/fr and /es, support.google.com/gemini with hl=fr and hl=es), so the kit quotes the menus as the founder sees them.

| | French | Spanish |
|---|---|---|
| ChatGPT, web | Paramètres, Personnalisation, « Activer la personnalisation », champ Instructions personnalisées | Configuración, Personalización, «Activar personalización», campo Instrucciones personalizadas |
| ChatGPT, mobile | Paramètres, Personnaliser ChatGPT | Configuración, Personalizar ChatGPT |
| ChatGPT, limit | « jusqu'à 1 500 caractères » (Free et Go), 5 000 (Plus et au-delà) | «hasta 1500 caracteres» (Free y Go), 5000 (Plus y superiores) |
| ChatGPT, project | menu Plus d'options (•••), Paramètres du projet | menú de más opciones (•••), Ajustes del proyecto |
| Claude, account | vos initiales en bas à gauche, « Paramètres », « Votre Claude », « Instructions » | "Configuración", "Tu Claude", "Instrucciones" |
| Claude, project | « Définir les instructions du projet »; cinq projets au plus en gratuit | "Establecer instrucciones del proyecto"; cinco proyectos como máximo en la cuenta gratuita |
| Gemini, skill | barre latérale, Personnaliser (sous Plus si absent), Compétences, Créer, Créer manuellement; avoir au moins 18 ans, Conserver l'activité | barra lateral, Personalizar (en Más si no aparece), Habilidades, Crear, Crear manualmente; ser mayor de 18 años, Guardar actividad |

## What this means for the two sizes

The short file (1,500 characters at most) fits the smallest field that exists everywhere: ChatGPT custom instructions on Free and Go. It also goes into Claude's account instructions.

The full file (8,000 characters at most) goes into a ChatGPT project, a Claude project or a Gemini skill. None of the three publishes a limit for that field, so 8,000 is Tonal's own cap, kept for one reason: a file the founder can read in full in five minutes is a file the founder will keep up to date. The two-size design holds; only the targets changed.
