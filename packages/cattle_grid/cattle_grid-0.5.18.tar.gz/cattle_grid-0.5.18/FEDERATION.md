# Federation

## Supported federation protocols and standards

cattle_grid does some version of ActivityPub on the Fediverse side.
The versions on the other side are cattle_grid specific, please
read the documentation below.

As mentioned in [Processed Activities](#processed-activities), cattle_grid
handles a limit set of things:

* Managing Actor Profiles
* Managing Followers / Following
* Distributing activities where they are meant to go (in both directions)

> [!NOTE]
> cattle_grid has [extensions](https://bovine.codeberg.page/cattle_grid/extensions/).
> This means it is easy to make cattle_grid act very differently dependent on
> the use case.
>
> e.g. the [muck_out](https://bovine.codeberg.page/muck_out/) extension restricts
> processing to a subset of normalized and validated objects and activities.

## Supported FEPs

* [FEP-67ff: FEDERATION.md](https://codeberg.org/fediverse/fep/src/branch/main/fep/67ff/fep-67ff.md)
* [FEP-f1d5: NodeInfo in Fediverse Software](https://codeberg.org/fediverse/fep/src/branch/main/fep/f1d5/fep-f1d5.md)
* [FEP-2277: ActivityPub core types](https://codeberg.org/fediverse/fep/src/branch/main/fep/2277/fep-2277.md), in the sense that activities have an actor property

## ActivityPub

### Processed Activities

cattle_grid has handling for `Follow`, `Accept`, `Undo`,
`Block`, `Reject`, and `Delete` activities. Handling
for `Move` is planned ([cattle_grid#237](https://codeberg.org/bovine/cattle_grid/issues/237)).

For further details, see [ActivityPub Processing](https://bovine.codeberg.page/cattle_grid/architecture/activitypub/)
and in particular, the AsyncAPI definition.

When an actor is updated, cattle_grid sends out an `Update` activity for the actor.
If an actor automatically accepts followers, cattle_grid sends out `Accept` activities
for the actor.


### Endpoints

See the OpenAPI document in the documentation.

## Additional documentation

* [Documentation](https://bovine.codeberg.page/cattle_grid/)
