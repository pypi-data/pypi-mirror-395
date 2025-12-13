# Testing

If you build on top on cattle_grid, you will want to test your code.
The references on the left contain exported methods that are useful
for writing your own tests. Some of their usage is also discussed
in [writing your extension](../extensions/index.md).

Furthermore, the are descriptions of the methods available to do
Behavior Driven Development.

## Testing configuration

By creating a config file such as

```toml title="config/testing.toml"
[testing]
enabled = true

[[testing.accounts]]
name = "user"
password = "pass"
permissions = ["admin"]

actors = [{ name = "test", handle = "test", base_url = "http://abel" }]
```

one can create automatically create test accounts
on startup. Similarly, by adding elements to the actor
list, actors will be automatically created.

We note that accounts are created on startup of the cattle_grid
server component.
