# Changes

## 0.5.18

* Ensure queue names are unique [cattle_grid#292](https://codeberg.org/bovine/cattle_grid/issues/292)
* Repair incorrect import in docs [cattle_grid#290](https://codeberg.org/bovine/cattle_grid/issues/290)
* Add link to FEDERATION.md on docs index [cattle_grid#284](https://codeberg.org/bovine/cattle_grid/issues/284)
* Add `AccountRequester` [cattle_grid#285](https://codeberg.org/bovine/cattle_grid/issues/285)
* Add frontend.base_url to required parameters for bdd tests [cattle_grid#286](https://codeberg.org/bovine/cattle_grid/issues/286)

## 0.5.17

* Ensure followers / following are unique [cattle_grid#282](https://codeberg.org/bovine/cattle_grid/issues/282)
* Improve import times for certain parts [cattle_grid#281](https://codeberg.org/bovine/cattle_grid/issues/281)
* Link to BDD reports from main docs [cattle_grid#278](https://codeberg.org/bovine/cattle_grid/issues/278)
* Make setting value of PropertyValue to null impossible [cattle_grid#279](https://codeberg.org/bovine/cattle_grid/issues/279)
* add `python -mcattle_grid install verify` command

## 0.5.16

* Add step to introduce actor to context [cattle_grid#266](https://codeberg.org/bovine/cattle_grid/issues/266)
* Include message body in error message [cattle_grid#269](https://codeberg.org/bovine/cattle_grid/issues/269)
* Migrate steps into package [cattle_grid#274](https://codeberg.org/bovine/cattle_grid/issues/274)
* improvements to docs [cattle_grid#272](https://codeberg.org/bovine/cattle_grid/issues/272)
* Improve BDD environment.py [cattle_grid#271](https://codeberg.org/bovine/cattle_grid/issues/271)
* Rename routing key [cattle_grid#275](https://codeberg.org/bovine/cattle_grid/issues/275)
* Fix bug for create_actor RPC call [cattle_grid#273](https://codeberg.org/bovine/cattle_grid/issues/273)

## 0.5.15

* Implement history for events [cattle_grid#240](https://codeberg.org/bovine/cattle_grid/issues/240)
* Set amqp_url in test [cattle_grid#267](https://codeberg.org/bovine/cattle_grid/issues/267)
* Move property value steps to shared steps folder
* Repair BDD step docstring [cattle_grid#268](https://codeberg.org/bovine/cattle_grid/issues/268)
* HTML Display incorrectly reacted to interactions with non managed activities
* BDD Tests: Check if errors in stream for user, and if yes print them [roboherd#62](https://codeberg.org/bovine/roboherd/issues/62)

## 0.5.14

* Use ApplicationConfig for alembic [cattle_grid#260](https://codeberg.org/bovine/cattle_grid/issues/260)
* Improve "Bob" follows "Alice" [cattle_grid#263](https://codeberg.org/bovine/cattle_grid/issues/263)
* randomly choose host for BDD tests [cattle_grid#264](https://codeberg.org/bovine/cattle_grid/issues/264)
* remove special config variable CATTLE_GRID_MQ and instead rely on configuration [cattle_grid#262](https://codeberg.org/bovine/cattle_grid/issues/262)
* Provide better debug output on asserts [cattle_grid#265](https://codeberg.org/bovine/cattle_grid/issues/265)
* Add config variable for AMQP RPC call timeouts
* Update config variables in resources [cattle_grid#257](https://codeberg.org/bovine/cattle_grid/issues/257)
* Simple storage now adds a default value for `@context` [cattle_grid#258](https://codeberg.org/bovine/cattle_grid/issues/258)

## 0.5.13

* Document using `@hey-api` EventSource [cattle_grid#218](https://codeberg.org/bovine/cattle_grid/issues/218)
* Add method to check if simple_storage is configured correctly [cattle_grid#256](https://codeberg.org/bovine/cattle_grid/issues/256)
* Cleaned up presentation of the database model [cattle_grid#254](https://codeberg.org/bovine/cattle_grid/issues/254)
* Check that the base_url is allowed [cattle_grid#255](https://codeberg.org/bovine/cattle_grid/issues/255)
* Enabling using form data with simple_register
* Enable creating an account on registration with simple_register
* Expose more methods in `cattle_grid.activity_pub`.
* publish npm to codeberg [cattle_grid#250](https://codeberg.org/bovine/cattle_grid/issues/250)
* Fix content-type for SSEs in openapi [cattle_grid#251](https://codeberg.org/bovine/cattle_grid/issues/251)
* Repair CLI command [cattle_grid#249](https://codeberg.org/bovine/cattle_grid/issues/249)
* Add documentation on how to write configuration for extensions [cattle_grid#245](https://codeberg.org/bovine/cattle_grid/issues/245)
* Fix and harden reporting [cattle_grid#247](https://codeberg.org/bovine/cattle_grid/issues/247)

## 0.5.12

* better document testing features [cattle_grid#246](https://codeberg.org/bovine/cattle_grid/issues/246)
* Fix missing preferredUsername in `Update(Actor)` [cattle_grid#244](https://codeberg.org/bovine/cattle_grid/issues/244)
* Improve extension documentation [cattle_grid#241](https://codeberg.org/bovine/cattle_grid/issues/241)
* improved exchange name scheme and usage [cattle_grid#243](https://codeberg.org/bovine/cattle_grid/issues/243)
* cleanup requester and publisher dependencies [catlte_grid#242](https://codeberg.org/bovine/cattle_grid/issues/242)
* rename db_uri -> db_url and amqp_uri -> amqp_url
* Remove null values from webfinger response [cattle_grid#238](https://codeberg.org/bovine/cattle_grid/issues/238)
* First version of FEDERATION.md [cattle_grid#231](https://codeberg.org/bovine/cattle_grid/issues/231)
* Repair CI BDD tests configuration [cattle_grid#234](https://codeberg.org/bovine/cattle_grid/issues/234)

## 0.5.11

- `features/steps/obj.py` can theoretically allow running tests against other Fediverse platorms.
- New step functions [cattle_grid#230](https://codeberg.org/bovine/cattle_grid/issues/230)
- Build report docs even when one test fails [cattle_grid#232](https://codeberg.org/bovine/cattle_grid/issues/232)

## 0.5.10

- Rework followers/following collection handling [cattle_grid#34](https://codeberg.org/bovine/cattle_grid/issues/34)
- Update readme.md [cattle_grid#160](https://codeberg.org/bovine/cattle_grid/issues/160)
- Only publish method information for extensions, if is has elements [cattle_grid#180](https://codeberg.org/bovine/cattle_grid/issues/180)
- Improved instructions for BDD [cattle_grid#227](https://codeberg.org/bovine/cattle_grid/issues/227)
- Allow using "{actor_id}/followers" to address followers
- Install muck_out for ci tests [cattle_grid#226](https://codeberg.org/bovine/cattle_grid/issues/226)

## 0.5.9

- Migrate to [faststream 0.6](https://faststream.ag2.ai/latest/release/#v060)
- Add `manuallyApprovesFollowers` to Actor properties

## 0.5.8

- For AMQP use direct reply when appropriate [cattle_grid#215](https://codeberg.org/bovine/cattle_grid/issues/215)
- Make `fastapi[standard]` a dependency [cattle_grid#223](https://codeberg.org/bovine/cattle_grid/issues/223)

## 0.5.7

- Repair CLI command [cattle_grid#217](https://codeberg.org/bovine/cattle_grid/issues/217)
- Update to mkdocs-awesome-nav
- New docs group in pyproject.toml
- Add AccountName to cattle_grid.dependencies.account [cattle_grid#216](https://codeberg.org/bovine/cattle_grid/issues/216)
- Cleanup dependencies [cattle_grid#220](https://codeberg.org/bovine/cattle_grid/issues/220)
- Add appropriate extras for test and dockerfile [cattle_grid#221](https://codeberg.org/bovine/cattle_grid/issues/221)

## 0.5.6

- Use discriminator for better interface [cattle_grid#219](https://codeberg.org/bovine/cattle_grid/issues/219)
- publish to additional routing keys [cattle_grid#214](https://codeberg.org/bovine/cattle_grid/issues/214)
- improve error message [cattle_grid#210](https://codeberg.org/bovine/cattle_grid/issues/210)
- remove dependency on fediverse-pasture [cattle_grid#212](https://codeberg.org/bovine/cattle_grid/issues/212)
- Update pyproject.toml to new syntax

## 0.5.5

- Use publisher instead of broker [cattle_grid#204](https://codeberg.org/bovine/cattle_grid/issues/204)
- Add additional CI configuration [cattle_grid#202](https://codeberg.org/bovine/cattle_grid/issues/202)
- Improve documentation display. [cattle_grid#203](https://codeberg.org/bovine/cattle_grid/issues/203)
- Add appropriate `.npmignore`. [cattle_grid#208](https://codeberg.org/bovine/cattle_grid/issues/208)
- Switch a lot rabbitmq queues to be durable

## 0.5.4

- Add link to code into html display docs [cattle_grid#200](https://codeberg.org/bovine/cattle_grid/issues/200)
- Improve html display (sanitization, footer) [cattle_grid#199](https://codeberg.org/bovine/cattle_grid/issues/199)
- Add replies / shares /likes tracking to html display [cattle_grid#196](https://codeberg.org/bovine/cattle_grid/issues/196)
- Ensure basic startup without configuration [cattle_grid#197](https://codeberg.org/bovine/cattle_grid/issues/197)
- Document redirecting using ShouldServe [cattle_grid#194](https://codeberg.org/bovine/cattle_grid/issues/194)
- Add check for x_ap_location to html_display [cattle_grid#195](https://codeberg.org/bovine/cattle_grid/issues/195)
- Repair end 2 end tests [cattle_grid#162](https://codeberg.org/bovine/cattle_grid/issues/162)

## 0.5.3

- Implement redirect behavior for html_display [cattle_grid#192](https://codeberg.org/bovine/cattle_grid/issues/192)
- Add replies to triggers [cattle_grid#190](https://codeberg.org/bovine/cattle_grid/issues/190)
- Add authorization check to html display [cattle_grid#193](https://codeberg.org/bovine/cattle_grid/issues/193)
- Added export mechanism to html_display [cattle_grid#188](https://codeberg.org/bovine/cattle_grid/issues/188)
- Fix typo in cattle drive [cattle_grid#191](https://codeberg.org/bovine/cattle_grid/issues/191)

## 0.5.2

- Repair usage of build_args in docker pipeline

## 0.5.1

- Improve documentation of `cattle_grid.dependencies`
- Add extension for relationships [cattle_grid#147](https://codeberg.org/bovine/cattle_grid/issues/147)

## 0.5.0

- Add warnings to CLI command line [cattle_grid#177](https://codeberg.org/bovine/cattle_grid/issues/177)
- Add permalinks to toc [cattle_grid#178](https://codeberg.org/bovine/cattle_grid/issues/178)
- Added `py.typed` file [cattle_grid#179](https://codeberg.org/bovine/cattle_grid/issues/179)
- Move some dependencies to internal [cattle_grid#181](https://codeberg.org/bovine/cattle_grid/issues/181)
- Refactor how stuff is published and resolved [cattle_grid#182](https://codeberg.org/bovine/cattle_grid/issues/182)

## 0.4.3

- Add exception middleware to root broker [cattle_grid#170](https://codeberg.org/bovine/cattle_grid/issues/170)
- Add info on method_information to cattle drive docs [cattle_grid#167](https://codeberg.org/bovine/cattle_grid/issues/167)
- Ensure sqlalchemy connections are properly closed [cattle_grid#164](https://codeberg.org/bovine/cattle_grid/issues/164)
- Actors now forward to their html page [cattle_grid#171](https://codeberg.org/bovine/cattle_grid/issues/171)
- Added deletion handling to extensions [cattle_grid#175](https://codeberg.org/bovine/cattle_grid/issues/175)
- Add `add_url`, `remove_url` to `update_actor` method actions
- Add docs for html_display extension
- Repair typescript errors when building js module docs

## 0.4.2

- Run alembic from main function [cattle_grid#157](https://codeberg.org/bovine/cattle_grid/issues/157)
- Update JS dependencies [cattle_grid#169](https://codeberg.org/bovine/cattle_grid/issues/169)
- Ensure more exceptions are passed to the account
- Display profile in html display [cattle_grid#168](https://codeberg.org/bovine/cattle_grid/issues/168)
- Add basic infrastructure for serving HTML content
- Add `cattle_grid.fastapi` to include `ActivityResponse`.
- Add ability to test extensions with mocked broker
- Enable extensions to configure rewrite rules [cattle_grid#166](https://codeberg.org/bovine/cattle_grid/issues/166)
- Add `publish_object` as a test in the simple storage feature
- Use `publish_activity` in `publish_object` [cattle_grid#163](https://codeberg.org/bovine/cattle_grid/issues/163)

## 0.4.1

- Add missing asyncpg dependency [cattle_grid#159](https://codeberg.org/bovine/cattle_grid/issues/159)

## 0.4.0

- Migrate to sqlalchemy [cattle_grid#148](https://codeberg.org/bovine/cattle_grid/issues/148)
- Harden extensions to work with empty config [cattle_grid#156](https://codeberg.org/bovine/cattle_grid/issues/156)
- Add redirect for html header to docs [cattle_grid#123](https://codeberg.org/bovine/cattle_grid/issues/123)
- Migrate cattle_grid.auth to sqlalchemy [cattle_grid#154](https://codeberg.org/bovine/cattle_grid/issues/154)

## 0.3.8

- Remove `@async_run_until_complete` [cattle_grid#152](https://codeberg.org/bovine/cattle_grid/issues/152)
- Refactor `cattle_grid.tools` packaging [cattle_grid#145](https://codeberg.org/bovine/cattle_grid/issues/145)
- Cleanup __main__ [cattle_grid#149](https://codeberg.org/bovine/cattle_grid/issues/149)
- Repair heartbeat [cattle_grid#144](https://codeberg.org/bovine/cattle_grid/issues/144)

## 0.3.7 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/12186))

- Add new methods to `cattle_grid.manage` [cattle_grid#140](https://codeberg.org/bovine/cattle_grid/issues/140)
- Improve pydantic objects in simple storage [cattle_grid#141](https://codeberg.org/bovine/cattle_grid/issues/141)
- Extracted server sent events to `cattle_grid.tools.fastapi` [cattle_grid#142](https://codeberg.org/bovine/cattle_grid/issues/142)
- Automatically add actors to account for testing [cattle_grid#139](https://codeberg.org/bovine/cattle_grid/issues/139)

## 0.3.6 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10774))

- Add `subscribe_on_account_exchange` to extensions [cattle_grid#135](https://codeberg.org/bovine/cattle_grid/issues/135)
- Refactor usage of testing fixtures [cattle_grid#137](https://codeberg.org/bovine/cattle_grid/issues/137)
- Add `cattle_grid.dependencies.CommittingSqlSession` [cattle_grid#134](https://codeberg.org/bovine/cattle_grid/issues/134)
- Removed superfluous command in package.json of the js lib [cattle_grid#136](https://codeberg.org/bovine/cattle_grid/issues/136)
- Add `cattle_grid.manage.AccountManager` [cattle_grid#133](https://codeberg.org/bovine/cattle_grid/issues/133)
- Add automatic setup for test accounts [cattle_grid#132](https://codeberg.org/bovine/cattle_grid/issues/132)

## 0.3.5 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10744))

- Add `actors show/modify` commands to `python -mcattle_grid`. [cattle_grid#128](https://codeberg.org/bovine/cattle_grid/issues/128)
- Add annotations for  Config [cattle_grid#130](https://codeberg.org/bovine/cattle_grid/issues/130)
- Add method to retrieve ActorForAccount by id [cattle_grid#129](https://codeberg.org/bovine/cattle_grid/issues/129). The behavior is encapsulated in `cattle_grid.manage.ActorManager`.
- Add `include_router` to Extension [cattle_grid#122](https://codeberg.org/bovine/cattle_grid/issues/122)
- Add a logo [cattle_grid#126](https://codeberg.org/bovine/cattle_grid/issues/126)
- Document how to install on single domain [cattle_grid#119](https://codeberg.org/bovine/cattle_grid/issues/119)
- Add published to actors [cattle_grid#124](https://codeberg.org/bovine/cattle_grid/issues/124)
- Improve sql session creation [cattle_grid#125](https://codeberg.org/bovine/cattle_grid/issues/125)

## 0.3.4 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10739))

- Enable creating reports [cattle_grid#103](https://codeberg.org/bovine/cattle_grid/issues/103)
- Fix simple_storage [cattle_grid#118](https://codeberg.org/bovine/cattle_grid/issues/118)

## 0.3.3 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10591))

- Reenable cli test on CI [cattle_grid#37](https://codeberg.org/bovine/cattle_grid/issues/37)
- Repair `cattle_grid new-config` [cattle_grid#117](https://codeberg.org/bovine/cattle_grid/issues/117)
- Add curl to build docker file
- Add actor related annotations to `cattle_grid.dependencies.processing` [cattle_grid#113](https://codeberg.org/bovine/cattle_grid/issues/113)
- Rename msg to message [cattle_grid#112](https://codeberg.org/bovine/cattle_grid/issues/112)
- Allow setting response class for extensions [cattle_grid#115](https://codeberg.org/bovine/cattle_grid/issues/115)

## 0.3.2 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10577))

- Stop requiring the db_uri argument in global_container.alchemy_database [cattle_grid#108](https://codeberg.org/bovine/cattle_grid/issues/108)
- Introduce `cattle_grid.dependencies.SqlSession` [cattle_grid#109](https://codeberg.org/bovine/cattle_grid/issues/109)
- Introduce `cattle_grid.dependencies.processing.MessageActor` [cattle_grid#111](https://codeberg.org/bovine/cattle_grid/issues/111)
- Improve handling of actor groups in CLI
- Repair auto increment for actor group table

## 0.3.1 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10557))

- Repair reload for extensions run [cattle_grid#105](https://codeberg.org/bovine/cattle_grid/issues/105)

## 0.3.0 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10442))

- Add a simple method rewriting [cattle_grid#101](https://codeberg.org/bovine/cattle_grid/issues/101)
- Enable configuring fakeredis as the key value database [cattle_grid#104](https://codeberg.org/bovine/cattle_grid/issues/104)
- Improved reported [cattle_grid#14](https://codeberg.org/bovine/cattle_grid/issues/14)
- Add a run command for extensions [cattle_grid#99](https://codeberg.org/bovine/cattle_grid/issues/99)
- remove cattle_grid.config.messaging [cattle_grid#100](https://codeberg.org/bovine/cattle_grid/issues/100)
- testing.fixtures now contains an sqlalchemy engine [cattle_grid#96](https://codeberg.org/bovine/cattle_grid/issues/96)
- Add client.gen to generate ts docs [cattle_grid#97](https://codeberg.org/bovine/cattle_grid/issues/97)

## 0.2.8 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/10324))

- Add command `account delete NAME` [cattle_grid#92](https://codeberg.org/bovine/cattle_grid/issues/92)
- Add command to prune deleted actors [cattle_grid#40](https://codeberg.org/bovine/cattle_grid/issues/40)
- Separated create and add identifier [cattle_grid#62](https://codeberg.org/bovine/cattle_grid/issues/62)
- Make more dependency injections generally available [cattle_grid#94](https://codeberg.org/bovine/cattle_grid/issues/94)
- Add missing docker tags to build step [cattle_grid#93](https://codeberg.org/bovine/cattle_grid/issues/93)
- Add a simple register extension [cattle_grid#52](https://codeberg.org/bovine/cattle_grid/issues/52)
- Update actor.profile instead of overwriting it [cattle_grid#91](https://codeberg.org/bovine/cattle_grid/issues/91)
- Improve documentation of TypeScript SDK [cattle_grid#89](https://codeberg.org/bovine/cattle_grid/issues/89)
- Add management of PropertyValue for actor [cattle_grid#57](https://codeberg.org/bovine/cattle_grid/issues/57)

## 0.2.7 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9769))

- Manually cancel FastAPI streams
- Add heartbeat to streaming [cattle_grid#88](https://codeberg.org/bovine/cattle_grid/issues/88)
- Add action to rename actors [cattle_grid#87](https://codeberg.org/bovine/cattle_grid/issues/87)
- Cleanup amqp queues
- Mark actors as deleted instead of deleting [cattle_grid#85](https://codeberg.org/bovine/cattle_grid/issues/85)
- Allow naming actors in the account [cattle_grid#76](https://codeberg.org/bovine/cattle_grid/issues/76)
- Include body in release
- Repair shared inbox [cattle_grid#84](https://codeberg.org/bovine/cattle_grid/issues/84)

## 0.2.6 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9700))

- Adjust trigger interface to match async api [cattle_grid#80](https://codeberg.org/bovine/cattle_grid/issues/80)
- Use node info object [cattle_grid#81](https://codeberg.org/bovine/cattle_grid/issues/81)
- Implement sharedInbox [cattle_grid#78](https://codeberg.org/bovine/cattle_grid/issues/78)

## 0.2.5 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9680))

- Added account name to InformationResponse [cattle_grid#77](https://codeberg.org/bovine/cattle_grid/issues/77)
- Check if public identifiers exist when creating actor [cattle_grid#75](https://codeberg.org/bovine/cattle_grid/issues/75)
- Repair streaming endpoints [cattle_grid#79](https://codeberg.org/bovine/cattle_grid/issues/79)
- Improve generate javascript package [cattle_grid#74](https://codeberg.org/bovine/cattle_grid/issues/74)

## 0.2.4 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9659))

- Document how to use cattle_grid.auth with caddy [cattle_grid#43](https://codeberg.org/bovine/cattle_grid/issues/43)
- More fine grained control of logging
- `/account/stream/type` now properly handles type [cattle_grid#68](https://codeberg.org/bovine/cattle_grid/issues/68)
- Start updating Account API to match Cattle Drive and start building typescript SDK [cattle_grid#67](https://codeberg.org/bovine/cattle_grid/issues/67)

## 0.2.3 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9654))

- Add basic permission structure for accounts [cattle_grid#47](https://codeberg.org/bovine/cattle_grid/issues/47)
- Handle another Undo Follow case [cattle_grid#60](https://codeberg.org/bovine/cattle_grid/issues/60)
- Add verified public identifiers [cattle_grid#50](https://codeberg.org/bovine/cattle_grid/issues/50)

## 0.2.2 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9648))

- Add configuration flag `processor_in_app` [cattle_grid#54](https://codeberg.org/bovine/cattle_grid/issues/54)
- Actors are now removed from account on delete [cattle_grid#56](https://codeberg.org/bovine/cattle_grid/issues/56)
- Remove `cattle_grid.exchange.server`, [cattle_grid#55](https://codeberg.org/bovine/cattle_grid/issues/55)

## 0.2.1 ([Milestone](https://codeberg.org/bovine/cattle_grid/milestone/9647))

- Enable building docker containers in CI [cattle_grid#49](https://codeberg.org/bovine/cattle_grid/issues/49)
- Implement `X-Cattle-Grid-Should-Serve` header [Issue#10](https://codeberg.org/bovine/cattle_grid/issues/10)
- Better naming of exchanges [cattle_grid#46](https://codeberg.org/bovine/cattle_grid/issues/46)
- Forbid certain account names [cattle_grid#45](https://codeberg.org/bovine/cattle_grid/issues/45)
