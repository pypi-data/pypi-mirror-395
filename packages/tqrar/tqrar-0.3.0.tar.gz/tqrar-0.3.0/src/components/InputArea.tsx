/**
 * Input Area Component - Kiro Style
 * Clean input area with autopilot toggle, checkpoint, and review buttons
 */

import React from 'react';
import { IExecutionSettings } from '../types';
import { AutopilotToggle } from './AutopilotToggle';
import { CheckpointButton, ICheckpoint } from './CheckpointButton';
import { ReviewButton, IChange } from './ReviewButton';
import { cn } from '../utils/classNames';

export interface IModelConfig {
  provider: 'openrouter' | 'openai' | 'anthropic' | string;
  model: string;
}

export interface IInputAreaProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
  placeholder?: string;
  currentModel?: IModelConfig;
  onModelChange?: (config: IModelConfig) => void;
  executionSettings?: IExecutionSettings;
  onExecutionSettingsChange?: (settings: IExecutionSettings) => void;
  // Checkpoint props
  checkpoints?: ICheckpoint[];
  onCreateCheckpoint?: () => void;
  onRestoreCheckpoint?: (checkpointId: string) => void;
  hasUnsavedChanges?: boolean;
  // Review props
  changes?: IChange[];
  onViewChange?: (changeId: string) => void;
  onAcceptAllChanges?: () => void;
  onRevertAllChanges?: () => void;
}

export const InputArea: React.FC<IInputAreaProps> = ({
  value,
  onChange,
  onSubmit,
  disabled = false,
  placeholder = 'Ask Tqrar...',
  // Model selection is now in Settings only
  // currentModel = { provider: 'anthropic', model: 'claude-3-5-sonnet-20241022' },
  // onModelChange,
  executionSettings = { mode: 'act', autoMode: true },
  onExecutionSettingsChange,
  checkpoints = [],
  onCreateCheckpoint,
  onRestoreCheckpoint,
  hasUnsavedChanges = false,
  changes = [],
  onViewChange,
  onAcceptAllChanges,
  onRevertAllChanges
}) => {
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  React.useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    }
  }, [value]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !disabled) {
        onSubmit();
      }
    }
  };

  const handleAutopilotChange = (enabled: boolean) => {
    if (onExecutionSettingsChange) {
      onExecutionSettingsChange({
        ...executionSettings,
        autoMode: enabled,
        // When autopilot is on, always use 'act' mode
        mode: enabled ? 'act' : executionSettings.mode
      });
    }
  };

  return (
    <div className="kiro-input-area tq-border-t tq-border-border-default tq-bg-bg-primary tq-flex-shrink-0">
      {/* Input container - Kiro style with everything inside the box */}
      <div className="tq-p-3">
        <div className="kiro-input-container tq-flex tq-flex-col tq-bg-bg-secondary tq-border tq-border-border-default tq-rounded-xl tq-transition-all focus-within:tq-border-accent-blue">
          {/* Textarea */}
          <textarea
            ref={textareaRef}
            className="kiro-textarea tq-w-full tq-bg-transparent tq-border-none tq-text-text-primary tq-text-sm tq-font-sans tq-resize-none tq-min-h-[40px] tq-max-h-[200px] tq-leading-relaxed tq-px-3 tq-pt-3 tq-pb-1 tq-outline-none"
            value={value}
            onChange={e => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            rows={1}
            disabled={disabled}
            aria-label="Message input"
          />
          
          {/* Bottom bar - all controls inside the input box */}
          <div className="tq-flex tq-items-center tq-justify-between tq-px-2 tq-py-2 tq-gap-2">
            {/* Left side: Autopilot toggle */}
            <div className="tq-flex tq-items-center tq-gap-1">
              {/* Autopilot Toggle - inside the input box */}
              <AutopilotToggle
                enabled={executionSettings.autoMode}
                onChange={handleAutopilotChange}
                disabled={disabled}
              />
            </div>

            {/* Right side: Optional buttons and Send */}
            <div className="tq-flex tq-items-center tq-gap-1">
              {/* Review Button - only show if there are changes */}
              {changes.length > 0 && onViewChange && onAcceptAllChanges && onRevertAllChanges && (
                <ReviewButton
                  changes={changes}
                  onViewChange={onViewChange}
                  onAcceptAll={onAcceptAllChanges}
                  onRevertAll={onRevertAllChanges}
                  isLoading={disabled}
                />
              )}

              {/* Checkpoint Button */}
              {onCreateCheckpoint && onRestoreCheckpoint && (
                <CheckpointButton
                  checkpoints={checkpoints}
                  onCreateCheckpoint={onCreateCheckpoint}
                  onRestoreCheckpoint={onRestoreCheckpoint}
                  hasChanges={hasUnsavedChanges}
                  isLoading={disabled}
                />
              )}

              {/* Send button */}
              <button
                className={cn(
                  'kiro-send-btn',
                  'tq-flex tq-items-center tq-justify-center',
                  'tq-w-7 tq-h-7 tq-rounded-lg',
                  'tq-bg-accent-blue tq-text-white',
                  'tq-border-none tq-cursor-pointer',
                  'tq-transition-all',
                  'hover:tq-bg-accent-blue-hover',
                  'active:tq-scale-95',
                  'disabled:tq-bg-bg-hover disabled:tq-text-text-muted disabled:tq-cursor-not-allowed disabled:tq-opacity-50'
                )}
                onClick={onSubmit}
                disabled={!value.trim() || disabled}
                title="Send message (Enter)"
                aria-label="Send message"
              >
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                  <path d="M8 12V4M8 4L4 8M8 4l4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
