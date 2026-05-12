# 1.0.0 (2026-05-12)


### Bug Fixes

* Conditionally apply `animate-pulse` class to the status bar based on the `loading` state. ([c465c0a](https://github.com/davnnis2003/MeetingMinds/commit/c465c0a39b3b346ce30faf1e298194baecd41481))
* force lowercase repository name in Docker image tags to ensure compatibility with GHCR naming conventions ([1c223af](https://github.com/davnnis2003/MeetingMinds/commit/1c223af657724d017f925c0e204a6e6afc505d64))
* increase transcription timeout, add error handling for Sona requests, and configure container restart policies with updated Whisper model ([f5c4470](https://github.com/davnnis2003/MeetingMinds/commit/f5c4470e5834c6d9d207259652ba0cae60ba97ea))
* move database table initialization to app startup to allow dynamic configuration in tests ([27b4ecb](https://github.com/davnnis2003/MeetingMinds/commit/27b4ecbcebcb6d39d4b5044e973d81527b7069e2))


### Features

* add .dockerignore files to root, backend, and frontend directories to exclude build artifacts and sensitive files ([4e6ebc5](https://github.com/davnnis2003/MeetingMinds/commit/4e6ebc5336b4ea5df0496f521e8c02762f292eb2))
* add alembic and greenlet dependencies and initialize api routers package ([18ed105](https://github.com/davnnis2003/MeetingMinds/commit/18ed105f6f9a373e3d8f00ccb9b466ffdd65883e))
* add detailed model download duration and processing time estimates to UI ([72ce61f](https://github.com/davnnis2003/MeetingMinds/commit/72ce61f3f606cce55564d402b314ec5346917771))
* Add frontend and backend run scripts, streamline the README, and update frontend package dependencies. ([e76f6ea](https://github.com/davnnis2003/MeetingMinds/commit/e76f6eae54bf9426be5da5bceb5162d2288d57dc))
* add JobsList component to track and download asynchronous processing tasks ([f744312](https://github.com/davnnis2003/MeetingMinds/commit/f744312f04c1ae7018b23acb7c6704d879a342bc))
* add manual release workflow to build and package macOS client via Nativefier ([20f73cb](https://github.com/davnnis2003/MeetingMinds/commit/20f73cb2d4c3b280e6174e4a1d31d865cac7dacb))
* add media input services, streaming YouTube transcription, and UI components for transcription and analysis views ([68b6d11](https://github.com/davnnis2003/MeetingMinds/commit/68b6d112b3ada9d86449ddcecc5a3c058549f9f6))
* add multi-arch support for Sona binary downloads in Dockerfile ([b255214](https://github.com/davnnis2003/MeetingMinds/commit/b255214608a1ecdf3ff788785874053268ec9a65))
* add SettingsPanel for OpenAI API key configuration and update backend environment variables ([ac17ede](https://github.com/davnnis2003/MeetingMinds/commit/ac17ede7fcb22f19fc822d40e2ef8ac795d395fc))
* add Sona transcription engine status monitoring and UI feedback to prevent processing during initialization ([651fea0](https://github.com/davnnis2003/MeetingMinds/commit/651fea0abd95af250899a8436a5b8cf9bdfb4de2))
* add support for M4A file uploads and include backend validation test ([e46869b](https://github.com/davnnis2003/MeetingMinds/commit/e46869b88daf5322179fcef0c526bef367addfeb))
* add support for OpenAI Whisper transcription via configurable system settings ([f730a9b](https://github.com/davnnis2003/MeetingMinds/commit/f730a9b6227a5d0eb778fba6457e8f6cafe0417a))
* add transcription_provider field to Job model and track provider used during processing ([4de7c57](https://github.com/davnnis2003/MeetingMinds/commit/4de7c576fba09a69b2575307c239dd54a6e77234))
* implement asynchronous job queueing with persistent status tracking and result downloads ([c9d6316](https://github.com/davnnis2003/MeetingMinds/commit/c9d6316a451dbc2ae4b2df47d99849a983307e3c))
* implement backend job processing with PostgreSQL, worker service, and API endpoints for job management ([ac07730](https://github.com/davnnis2003/MeetingMinds/commit/ac07730f0a7fa58ef5e8a30582d172e26331373f))
* implement comprehensive logging and error tracking across API and service layers ([e29d796](https://github.com/davnnis2003/MeetingMinds/commit/e29d79637a6719dfe72942a4f2d5ddf099d4e01e))
* implement frontend UI components, API service, and backend testing suite ([0a0a6e1](https://github.com/davnnis2003/MeetingMinds/commit/0a0a6e12a20298932039382d51e0028886dacc77))
* Implement real-time YouTube transcription with thread-safe Whisper and improved .gitignore ([198b4ff](https://github.com/davnnis2003/MeetingMinds/commit/198b4ff361a99ed64198d77a3564b67d1c473972))
* Implement YouTube transcription API with a fallback from captions to audio transcription and add a corresponding test. ([2c9fa5a](https://github.com/davnnis2003/MeetingMinds/commit/2c9fa5ae15254de684a92c2788c22164df3aa728))
* initialize routers package with documentation header ([5b43446](https://github.com/davnnis2003/MeetingMinds/commit/5b4344610c1933f340f9e6171b59b7c9d2ec5ce6))
* integrate OpenAI Whisper for audio transcription with configurable API key support ([4baf9e9](https://github.com/davnnis2003/MeetingMinds/commit/4baf9e90a6667e1b755d089cc564b1c04b36d42d))
* integrate semantic-release and automate MacOS client distribution to GitHub releases ([0dcf5ce](https://github.com/davnnis2003/MeetingMinds/commit/0dcf5ce844d9cfb2cfe39e88e2a83105a1f27999))
* Introduce a Makefile for streamlined development commands and update the README.md to reflect these new quick start instructions. ([2989212](https://github.com/davnnis2003/MeetingMinds/commit/2989212b24f0a91abef0c58abee57fd59d35002c))
* introduce MeetingMind application with meeting recording, transcription, and summarization capabilities. ([4d66e53](https://github.com/davnnis2003/MeetingMinds/commit/4d66e53479c2fa6045f7a0568710273dd45cbec8))
* migrate semantic-release configuration to standalone .releaserc.json file ([3691a86](https://github.com/davnnis2003/MeetingMinds/commit/3691a86976a39c3fb1efc1f8eb4d45663126bcb3))
* modularize backend routes and implement frontend API service for transcription and generation ([1072466](https://github.com/davnnis2003/MeetingMinds/commit/10724663bd1350067fcf40615709ca148492f8dc))
* redesign file upload component and add animated upcoming features roadmap section ([36cc3be](https://github.com/davnnis2003/MeetingMinds/commit/36cc3be56a3908182e6c1f8b5ced4bd586d550d7))
* Unify YouTube video download and transcription into a single API endpoint for streamlined processing. ([051d927](https://github.com/davnnis2003/MeetingMinds/commit/051d92729d7b390ededcb0b16b871c8c68fb8537))
* update YouTube transcript fetching logic and add integration tests for job queue processing ([67b5ce4](https://github.com/davnnis2003/MeetingMinds/commit/67b5ce47ea172d2f44c6ee88036d6bef8a1fe3d1))
* upgrade whisper model to distil-large-v3 with int8 quantization and add timeout to scribe transcription requests ([b234609](https://github.com/davnnis2003/MeetingMinds/commit/b23460965ff141cab38d2bdb4fda6c60cb2c3807))
