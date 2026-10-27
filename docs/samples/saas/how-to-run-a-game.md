# Run a game

How a host takes a room from lobby to results. Written for the host; players only need the room code.

## Host checklist

Before you start:

- [ ] Every player has joined and shows a ready state
- [ ] The role mix matches the player count; see [Roles](#roles)
- [ ] The three timers suit the group. New groups need longer discussion
- [ ] Video and voice are on only if everyone agreed to be on camera
- [ ] You know who is hosting. Only the host can start, end or change settings

## Roles

Each player gets one role, revealed privately at the start.

| Role | Team | What the player does |
| --- | --- | --- |
| Citizen | Town | No night action. Argues, votes, and tries to survive |
| Mafia | Mafia | Chooses a player to eliminate each night. Knows the other Mafia |
| Doctor | Town | Protects one player each night. A protected player survives an attack |
| Detective | Town | Investigates one player each night and learns their team |

Role counts are part of the game settings. The classic setup scales Mafia with player count; the advanced setup adds the Doctor and Detective. If a role is disabled, nobody is assigned it and the night step for that role does not appear.

## Phases

A game runs the same loop until one team wins.

| Phase | Who acts | What happens |
| --- | --- | --- |
| Night | Mafia, Doctor, Detective | Secret actions, in that order. Timed by the night timer |
| Morning | Everyone | The night result is announced: who was eliminated, and who was saved |
| Discussion | Everyone alive | Open chat and voice. Accusations, alibis, claims |
| Voting | Everyone alive | Each player votes once. Anonymous voting is a setting; when on, the tally appears without names |
| Result | Everyone | The eliminated player is revealed, the role is not |
| Results | Everyone | Final screen: winning team, per-player outcome, XP earned |

Dead players become spectators. They see the game but cannot speak in the main chat; the dead chat setting, when on, gives them a channel of their own.

## Timers

Three settings control pace. They belong to the room, not to the phase, so a change applies from the next phase.

| Setting | Default feel | Raise it when |
| --- | --- | --- |
| Night timer | Short, 30 to 45 seconds | New players are still learning the night actions |
| Discussion timer | Medium, 2 to 3 minutes | The group is large or playing remotely |
| Voting timer | Short, 30 seconds | Players tend to deliberate out loud and forget to vote |

## During the game

**As host, you can:**

- Pause between phases to explain a rule to a new player
- Change a timer before the next phase starts
- End the game early. Ending records the game as abandoned for every player

**As host, you cannot:**

- See another player's role. Host is not an observer role
- Change a vote after it is cast
- Re-add a player who left mid-game; they rejoin as a spectator

## Reading the end screen

The results screen shows the winning team, each player's role and outcome, and the XP awarded. Level, coins and rank update on the profile page. The recent games list keeps the mode, role, result and XP earned per game, which is the fastest way to see whether a role suits you.

## If the group is new

Run one practice round with all timers long and video off. The first game that fails is almost always a camera permission problem at the ten-second mark, not a rules problem.
