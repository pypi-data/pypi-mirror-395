// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module my-shared-drive-extension
 */
import { rtcContentProvider, yfile, ynotebook } from './filebrowser';
/**
 * Export the plugins as default.
 */
const plugins = [
    rtcContentProvider,
    yfile,
    ynotebook
];
export default plugins;
