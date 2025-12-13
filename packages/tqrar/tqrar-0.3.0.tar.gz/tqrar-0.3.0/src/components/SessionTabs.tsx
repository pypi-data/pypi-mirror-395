/**
 * Session Tabs Component
 * Shows active sessions as tabs
 */

import React from 'react';
import { ISession } from '../session';
import { cn } from '../utils/classNames';

export interface ISessionTabsProps {
  sessions: ISession[];
  activeSessionId: string | null;
  onSessionSelect: (id: string) => void;
  onSessionClose: (id: string) => void;
}

export const SessionTabs: React.FC<ISessionTabsProps> = ({
  sessions,
  activeSessionId,
  onSessionSelect,
  onSessionClose
}) => {
  // Log render state
  console.log('🏷️ [TABS] Rendering:', {
    activeSessionId,
    sessionCount: sessions.length,
    sessions: sessions.map(s => ({ id: s.id, title: s.title }))
  });
  
  // Don't show tabs if no active session
  if (!activeSessionId || sessions.length === 0) {
    console.log('🚫 [TABS] Not rendering (no active session or empty sessions)');
    return null;
  }

  return (
    <div className="tq-flex tq-gap-1 tq-overflow-x-auto tq-items-center">
      {sessions.map(session => (
        <div
          key={session.id}
          className={cn(
            'tq-flex tq-items-center tq-gap-1 tq-px-2 tq-py-1 tq-rounded tq-cursor-pointer tq-transition-colors tq-max-w-[160px]',
            session.id === activeSessionId
              ? 'tq-bg-bg-hover tq-text-text-primary'
              : 'tq-text-text-secondary hover:tq-bg-bg-hover hover:tq-text-text-primary'
          )}
          onClick={() => {
            console.log('👆 [TABS] Tab clicked:', session.id);
            onSessionSelect(session.id);
          }}
        >
          <span className="tq-flex-1 tq-truncate tq-text-xs">{session.title}</span>
          <button
            className="tq-text-text-muted hover:tq-text-text-primary tq-transition-colors tq-text-sm tq-leading-none tq-flex-shrink-0 tq-w-4 tq-h-4 tq-flex tq-items-center tq-justify-center"
            onClick={(e) => {
              e.stopPropagation();
              console.log('❌ [TABS] Close button clicked:', session.id);
              onSessionClose(session.id);
            }}
            title="Close session"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
};
