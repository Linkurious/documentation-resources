package com.linkurious.neo4jSearch;

import org.neo4j.graphdb.schema.AnalyzerProvider;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.custom.CustomAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizerFactory;
import org.apache.lucene.analysis.core.LowerCaseFilterFactory;
import org.apache.lucene.analysis.pattern.PatternReplaceFilterFactory;
import org.apache.lucene.analysis.miscellaneous.WordDelimiterGraphFilterFactory;
import org.apache.lucene.analysis.miscellaneous.ASCIIFoldingFilterFactory;
import java.io.IOException;
import java.io.UncheckedIOException;

public class CustomAnalyzerProvider extends AnalyzerProvider
{

    public static final String DESCRIPTION = "Linkurious custom analyzer for alphanumeric tokens (BETA)";
    public static final String ANALYZER_NAME = "linkurious-custom-analyzer";

    public CustomAnalyzerProvider()
    {
        super(ANALYZER_NAME);
    }

    @Override
    public Analyzer createAnalyzer()
    {
        try
        {
            return CustomAnalyzer.builder()
                    .withTokenizer(StandardTokenizerFactory.class)
                    .addTokenFilter(ASCIIFoldingFilterFactory.class, "preserveOriginal", "false")
                    .addTokenFilter(LowerCaseFilterFactory.class)
                    .addTokenFilter(PatternReplaceFilterFactory.class, "pattern", "([^a-z0-9])", "replacement", " ")
                    .addTokenFilter(WordDelimiterGraphFilterFactory.class, 
                                    "generateWordParts", "1", 
                                    "generateNumberParts", "1", 
                                    "catenateWords", "1", 
                                    "catenateNumbers", "1", 
                                    "catenateAll", "1",
                                    "splitOnCaseChange", "0",
                                    "preserveOriginal", "1",
                                    "splitOnNumerics", "0")
                    .build();
        }
        catch ( IOException e )
        {
            throw new UncheckedIOException(e);
        }
    }

    @Override
    public String description() {
        return DESCRIPTION;
    }
}