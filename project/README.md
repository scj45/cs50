# Library 504
### Video Demo:

[YouTube](https://youtu.be/QYKt9-xa1Xs)

### Description:
Welcome to Library 504! This is a web-app offering a platform for building, organising and keeping track of your very own Home Library.

The app consists of two folders and 6 files:
* :card_index_dividers: staticfiles
* :card_index_dividers: templates
* :page_with_curl: app.py
* :page_with_curl: library.db (this is the database! this is important)
* :page_with_curl: LICENSE.txt
* :page_with_curl: README.md (you're reading this now, very meta)
* :page_with_curl: requirements.txt
* :page_with_curl: schema.txt (in case you want to know what the database looks like)

In the staticfiles folder you'll find the error code [jpg](staticfiles/400.jpg) and [style.css](staticfiles/style.css) files.

The templates folder houses 11 files, which are all html files, used within the app as different pathway templates.

Think you have too many books? Not sure if you've already bought that sequel? Don't remember what you read two months ago? Library 504 is here to fix that! Here are the features included in the app for you:

* #### :classical_building: Registering VS Logging In:
The first time you use the app, click on 'Not a member? Register here' to create an account! This will lead you the the /register path where you will be led through a multi-step form where you register your name and contact details, and set up your username and password. If you've been here before, feel free to log in using your username and password.

* #### :books: Homepage:
Logging in will bring you to your homepage, where the latest 5 books you've interacted with are listed in table form. You'll see the footer along the bottom, and the navigation bar fixed permanently at the top. If you scroll down, an arrow will appear on your bottom right corner, which will bring you back up to the top without needing to scroll.

* #### :memo: Log:
Now you're ready to start building your library/collection! From the navigation bar, click through to the 'Log a book' option which takes you to the /log path. This is also a multi-step form, where you will be asked to provide the title, primary author's first and last name, publication year, which edition you own, how many copies you own, the book's genre and three main topics the book relates to. Genre is chosen from 24 checkboxes, and you may select all that apply. Upon submission you will the redirected to the homepage.

* #### :mag: Search:
Looking for something specific? Click on the 'Search' option from the menu bar, and you will be taken to the /search pathway. On the screen, you will see the search bar in the centre of the top, with a green submit button. Once you start typing, a cross will appear at the end of the bar for you to cancel any search term you change your mind about.
Once you click submit, the web app will comb through your book data find entries which contain the word you have searched. The match could occur in title, author, topics, publishing year etc.

* #### :thought_balloon: Browse:
Just browsing? That's fine too! Click 'Browse' to be taken through to /browse. Here you will find a complete display of every book in your database. Feel free to peruse this feature if you're just casually scrolling through to pick your next read!

* #### :closed_book: Finished a book:
Congrats on finishing the latest page turner! Now you can make a note of what you'd rate the book out of 5 so you can look back in a couple months' time and remember what you thought of this one. Just fill in the short form at the /finish pathway to log your read!

* #### :abacus: History:
The /history path lets you look at your user activity on the webapp so far, so you can see every book you've interacted with. It'll show you what action occurred with the book (e.g. logged or read) and the date and time of the activity.

> [!NOTE]
> Future Developments:
> Hopefully, as the web app grows and more feedback comes in, the code and design will continue developing, such as maybe including a helpful chatbot with book recommendations and also filtering or sorting the tables to your preference.

> [!TIP]
> Feedback:
> We love constructive criticism! Please send any (friendly, please) feedback to [stephaniecjat@gmail.com](mailto:stephaniecjat@gmail.com)
