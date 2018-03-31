import { configure } from '@storybook/react';

function loadStories() {
  require('../app/stories/stories.story.tsx');
}

configure(loadStories, module);
