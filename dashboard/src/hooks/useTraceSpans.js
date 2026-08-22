import { useCallback, useEffect, useRef, useState } from 'react';
import { sortSpansByStart } from '../lib/spans';
import { formatSupabaseError, supabase } from '../supabaseClient';

export function useTraceSpans(traceId) {
  const [spans, setSpans] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const requestId = useRef(0);

  const loadSpans = useCallback(async (activeTraceId) => {
    if (!activeTraceId) {
      setSpans([]);
      setErrorMessage('');
      setIsLoading(false);
      return;
    }

    const activeRequest = requestId.current + 1;
    requestId.current = activeRequest;
    setSpans([]);
    setErrorMessage('');
    setIsLoading(true);

    const { data, error } = await supabase
      .from('spans')
      .select('*')
      .eq('trace_id', activeTraceId)
      .order('started_at', { ascending: true });

    if (requestId.current !== activeRequest) return;

    if (error) {
      setErrorMessage(formatSupabaseError(error, 'Check the Supabase connection and try again.'));
      setIsLoading(false);
      return;
    }

    setSpans(sortSpansByStart(data ?? []));
    setIsLoading(false);
  }, []);

  useEffect(() => {
    loadSpans(traceId);

    return () => {
      requestId.current += 1;
    };
  }, [loadSpans, traceId]);

  return {
    spans,
    isLoading,
    errorMessage,
    reload: () => loadSpans(traceId),
  };
}
