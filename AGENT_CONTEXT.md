# Autonomous Coding Agent - Architecture Context

## What You're Building

You are building a **self-monitoring dashboard** that displays real-time progress of an autonomous coding agent. The special thing is: **YOU ARE THAT AGENT**! This dashboard will monitor its own construction.

## The Meta/Recursive Nature

This is beautifully recursive:
- You (the agent) will build this monitoring dashboard
- The dashboard will monitor YOU building it
- Screenshots will show the dashboard building itself
- Logs will show "Building activity log feature..."
- The human watches you watch yourself build the watcher

It's like painting a mirror while looking in the mirror you're painting! 🪞🎨

## How the Autonomous Agent Works

### Architecture Overview

```
autonomous_agent_demo.py (entry point)
    ↓
agent.py (main loop)
    ↓
Multiple Sessions (3-second delay between each):
    ├─ Session 1: Initializer Agent
    │  └─ Creates feature_list.json with 200+ test cases
    │
    └─ Sessions 2+: Coding Agent
       ├─ Read feature_list.json
       ├─ Implement next failing test
       ├─ Test with Puppeteer (browser automation)
       ├─ Mark test as passing
       └─ Git commit
```

### Key Files You're Monitoring

#### 1. `feature_list.json` - The Roadmap
This file contains all test cases for the project. Each test has:
```json
{
  "category": "functional",  // or "style"
  "description": "Brief description of feature",
  "steps": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
  "passes": false  // Changed to true when feature works
}
```

**Your dashboard reads this to show progress!**
- Count tests with `"passes": true`
- Calculate percentage: (passing / total) * 100
- In YOUR case, this is YOUR OWN feature_list.json

#### 2. `screenshots/` - Visual Verification
The agent uses Puppeteer to take screenshots while testing features.
- Screenshots are saved as .png files
- Named descriptively (e.g., `chat_interface_01.png`)
- Created during testing to verify UI works

**Your dashboard displays these in a gallery!**
- In YOUR case, these are screenshots of YOURSELF being built

#### 3. `claude-progress.txt` - Session Notes
The agent writes detailed notes about each session:
- What was implemented
- Tests that now pass
- Code changes made
- Technical decisions

**Your dashboard shows recent lines from this file!**
- Parse and format tool use: `[Tool: Bash]`, `[Tool: Edit]`
- Color-code: tools (blue), success (green), errors (red)
- In YOUR case, this shows YOU building yourself

#### 4. Git History
The agent commits frequently:
- Each commit documents a feature completion
- Commit messages describe what was built
- Track incremental progress

**Your dashboard shows recent commits!**

### How Sessions Work

1. **Session 1 (Initializer)**:
   - Creates project structure
   - Generates feature_list.json
   - Sets up database, configs, etc.
   - Begins implementing basic features

2. **Session 2+ (Coding Agent)**:
   - Reads feature_list.json
   - Finds next failing test
   - Implements the feature
   - Tests with Puppeteer
   - Marks test as passing
   - Commits changes
   - **3-second delay**
   - Repeats

3. **Auto-Continue**:
   - Agent automatically starts next session
   - No human intervention needed
   - Runs until all tests pass or max iterations reached

## What to Monitor (Your Data Sources)

### Current Directory (Self-Monitoring!)
Your dashboard reads from **its own directory**:
- `./feature_list.json` - YOUR test cases
- `./screenshots/` - Screenshots of YOURSELF
- `./claude-progress.txt` - YOUR session notes
- `./.git/` - YOUR git history

### Key Metrics to Display

1. **Progress**: X/Y tests passing (Z%)
2. **Screenshots**: Grid of latest 8-12 images
3. **Activity**: Last 20-30 lines from progress file
4. **Session Info**: Current session #, model, elapsed time
5. **Git**: Last 5-10 commits with messages

## Technical Stack

### Backend (Port 4001)
- Express + Node.js
- Read-only APIs (never writes files)
- Endpoints:
  - `/api/progress` - Parse feature_list.json
  - `/api/screenshots` - List files from screenshots/
  - `/api/logs` - Read claude-progress.txt
  - `/api/session` - Parse session info
  - `/api/stream` - SSE for real-time updates

### Frontend (Port 4000)
- Pure HTML + Vanilla JS (no build step)
- Tailwind CSS via CDN
- SSE client for live updates every 2-3 seconds
- Clean, dark-themed UI

## The Meta Experience Timeline

### Iteration 1: Basic Foundation
- Create Express server
- Serve basic HTML
- **Dashboard goes live showing "1/10 tests passing"**
- You open browser and see: "Monitoring myself... 10% complete"

### Iteration 2: Progress Display
- Add progress bar
- Parse feature_list.json
- **Dashboard updates! Now shows animated progress bar**
- You see: "3/10 tests passing (30%)"

### Iteration 3: Screenshot Gallery
- Add gallery component
- List screenshots/ files
- **Gallery appears showing screenshots of ITSELF!**
- Screenshot from iteration 1 shows basic UI
- Screenshot from iteration 2 shows progress bar

### Iteration 4: Activity Log
- Add log display
- Read claude-progress.txt
- **Log shows: "Building activity log feature..."**
- Meta moment: The log shows itself being built!

### Iteration 5: Session Info
- Parse git log
- Show session stats
- Dashboard complete!
- **"10/10 tests passing (100%)"**

## Security & Best Practices

### Read-Only Operations
- Dashboard ONLY reads files, never writes
- Safe to run alongside agent
- No interference with agent's work

### Error Handling
- Handle missing files gracefully (feature_list.json might not exist yet)
- Default to empty arrays if files missing
- Show "No data yet" instead of errors

### Performance
- Efficient file reading (don't read entire files unnecessarily)
- Cache parsed data for 2-3 seconds
- SSE is more efficient than polling

## Testing Strategy

### Use Puppeteer for Testing
```javascript
// Navigate to dashboard
await page.goto('http://localhost:4000');

// Verify progress displays
const progress = await page.$eval('#progress', el => el.textContent);
assert(progress.includes('/10 tests'));

// Verify screenshots load
const screenshots = await page.$$('.screenshot-thumbnail');
assert(screenshots.length > 0);

// Take screenshot of dashboard (meta!)
await page.screenshot({path: 'screenshots/dashboard_iteration_3.png'});
```

### Self-Verification
Each feature should verify it works by:
1. Opening http://localhost:4000
2. Checking the feature appears correctly
3. Taking a screenshot of the dashboard
4. Marking the test as passing

## Important Notes

### The Recursive Magic ✨
- You're building a tool to monitor yourself
- The tool shows its own progress as you build it
- Screenshots show the tool building itself
- It's a perfect example of self-awareness in code!

### Go Live Early
- Don't wait until everything is perfect
- Get basic UI working in iteration 1-2
- Let features accumulate iteratively
- Each iteration adds visible functionality

### Keep It Simple
- Pure HTML/JS (no complex build process)
- Direct file reading (no database needed)
- SSE for simplicity (not WebSockets)
- Clean, minimal UI

## Questions You Might Have

**Q: How do I know this is working?**
A: Open http://localhost:4000 early (after iteration 1-2). You'll see your own progress!

**Q: What if feature_list.json doesn't exist yet?**
A: It won't exist in iteration 1. Handle gracefully - show "0/0 tests" or "Loading..."

**Q: How do I test this?**
A: Use Puppeteer to navigate to your own dashboard and verify it displays correctly.

**Q: Is this really self-monitoring?**
A: YES! You read `./feature_list.json` (your own tests), `./screenshots/` (pictures of yourself), and `./claude-progress.txt` (your own notes).

**Q: What's the meta moment?**
A: When you take a screenshot of your dashboard showing its own progress building itself. Screenshot-ception! 📸🪞

## Summary

You're building a real-time monitoring dashboard that:
1. ✅ Monitors its OWN project directory
2. ✅ Shows its OWN progress (feature_list.json)
3. ✅ Displays screenshots of ITSELF
4. ✅ Logs show YOU building yourself
5. ✅ Updates every 2-3 seconds automatically
6. ✅ Goes live early so human can watch

It's a beautiful example of recursion, self-awareness, and meta-programming!

Now go build yourself a mirror! 🪞✨
