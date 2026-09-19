import React from 'react';
import { RotateCcw, Wrench, RefreshCw, Flame, Trash2, AlertTriangle } from 'lucide-react';

interface HierarchyBadgeProps {
  pathway: string;
  size?: 'sm' | 'md' | 'lg';
  showTier?: boolean;
}

export const HierarchyBadge: React.FC<HierarchyBadgeProps> = ({
  pathway,
  size = 'md',
  showTier = false,
}) => {
  const p = pathway.toUpperCase();

  let colorClasses = 'bg-slate-100 text-slate-700 border-slate-300';
  let tierText = '';
  let Icon = RotateCcw;

  if (p.includes('REUSE')) {
    colorClasses = 'bg-emerald-50 text-emerald-800 border-emerald-300';
    tierText = 'Tier 1';
    Icon = RotateCcw;
  } else if (p.includes('REPAIR')) {
    colorClasses = 'bg-teal-50 text-teal-800 border-teal-300';
    tierText = 'Tier 2';
    Icon = Wrench;
  } else if (p.includes('RECYCLE')) {
    colorClasses = 'bg-blue-50 text-blue-800 border-blue-300';
    tierText = 'Tier 3';
    Icon = RefreshCw;
  } else if (p.includes('RECOVER')) {
    colorClasses = 'bg-amber-50 text-amber-800 border-amber-300';
    tierText = 'Tier 4';
    Icon = Flame;
  } else if (p.includes('SPECIALIZED') || p.includes('HAZARDOUS')) {
    colorClasses = 'bg-red-50 text-red-800 border-red-300';
    tierText = 'Specialized';
    Icon = AlertTriangle;
  } else if (p.includes('DISPOSE')) {
    colorClasses = 'bg-rose-50 text-rose-800 border-rose-300';
    tierText = 'Tier 5';
    Icon = Trash2;
  }

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-2.5 py-1 text-xs gap-1.5 font-medium',
    lg: 'px-3.5 py-1.5 text-sm gap-2 font-semibold',
  }[size];

  const iconSizes = {
    sm: 12,
    md: 14,
    lg: 16,
  }[size];

  return (
    <span
      className={`inline-flex items-center rounded-full border shadow-sm ${colorClasses} ${sizeClasses}`}
    >
      <Icon size={iconSizes} className="shrink-0" />
      {showTier && (
        <span className="opacity-75 text-[10px] font-bold uppercase tracking-wider mr-0.5">
          [{tierText}]
        </span>
      )}
      <span>{pathway}</span>
    </span>
  );
};
