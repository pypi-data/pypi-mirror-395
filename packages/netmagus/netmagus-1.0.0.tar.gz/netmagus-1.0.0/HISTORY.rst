=======
History
=======

0.10.0 (2020-12-17)
-------------------
* refactor SelectDrop to have more user friendly arg names

0.9.0 (2020-04-30)
------------------
* add new SelectDrop form object for drag-drop selection lists

0.8.0 (2019-10-02)
------------------
* changes to support Python 3.6+ only
* add new namespace at NetMagusSession.screens to store screens used in a session

0.7.8 (2019-10-01)
------------------
* minor doc fixes
* update to some dependency versions and TOX configs for builds

0.7.5 (2017-10-05)
------------------
* change the package's use of the loglevel arg from NM GUI.  The log level set in the GUI admin screen for a formula is now used to suppress all messages below the target for the entire python `logging` module. This changes default behavior for logging from the formula and all dependencies.  Formula writers may explicitly override this behavior within their formulas as desired with the standard `logging.disable()` method.
* add exception logging in case of import error when loading a user's formula module.  This will make it easier for formula writers to understand if they have problems in their module's `run()` method.
* add a default handler for the TryAgain button inside the `ScreenBase.handle_back_button` method

0.7.4 (2017-08-25)
------------------
* renamed the internal NetMagusSession.start() method to _start since it is not intended to be part of user API

0.7.2 (2017-08-22)
------------------
* Add new ScreenBase() arg to allow over-ride of default behavior to wipe the HTML pop-up area afer each screen passes user data validation

0.7.1 (2017-08-21)
------------------
* changed session.display_screen() to re-raise a CancelButtonPressed exception to be handled by the caller

0.7.0 (2017-08-18)
------------------
* add new ScreenBase abstract base class
