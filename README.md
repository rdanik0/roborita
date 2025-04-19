## Development guidelines (MUST-READ for the dev-team)
### Keep in mind
1. Use **meaningful** comments to explain non-obvious code logic.
2. Keep your code **well-formatted**.
3. Avoid leaving temporary/debugging code.
4. Keep pull requests **focused and not too large** — ideally, solve **one** task or feature per PR.
5. Make sure your branch names follow the `feature/name` structure.

### Do like that

1. Clone the repository:\
`git clone https://github.com/rdanik0/roborita.git`

2. Open `dev branch`:\
`git checkout dev`

3. Create a new branch with your feature name:\
`git checkout -b feature/my-new-feature`

4. Work on the code:\
`git add .`\
`git commit -m "something important bla-bla-bla"`

5. Push the feature after being done:\
`git push origin feature/my-new-feature`

> [!IMPORTANT]
> Next steps only if the code is not a experimental feature...

6. Triple-check everything and make a **Pull Request** to the `dev branch` on GitHub.

7. **Wait**.

> [!WARNING]
> Do not merge the dev branch and the main branch until the code is 100% stable and working. 

Violators of any of the rules will be used as a whiteboard for brainstorming sessions. Follow the guidelines.
