# crosslink-ml-hn  [![Build Status](https://travis-ci.org/liviu-/crosslink-ml-hn.svg?branch=master)](https://travis-ci.org/liviu-/crosslink-ml-hn)

## Overview

Reddit bot to link from [/r/machinelearning](https://www.reddit.com/r/MachineLearning/) submissions to [HN](https://news.ycombinator.com/news) discussions for same URL submissions to encourage more discussion/engagement between communities.

[/u/hn_crosslinking_bot](https://www.reddit.com/user/hn_crosslinking_bot)

## To-do

I may or may not add any of these, but just to write down some potential improvements:
- [ ] Crosslink with /r/statistics and other subreddits
- [ ] Crosslink from HN (do they even allow bots?)
- [x] Normalise URLs before checking similarity
- [x] Only link if HN submission has over `x` number of comments
- [x] Check older HN submissions too
- [ ] Add a notification system (but not email pls)
    - [ ] Notify on new comment
    - [ ] Notify on error
    - [ ] Notify on receiving new PM/replies
