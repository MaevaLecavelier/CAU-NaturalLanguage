
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.Scanner;

public class luceneProject {

    public static void main(String[] args){
        int verbose = 0;
        long startTime, endTime, diffTime;
        // create analyzer
        StandardAnalyzer analyzer = new StandardAnalyzer();
        System.out.println("\nWelcome to Lucene indexing and query system.\nIf you want to index files, just add an argument (for example '1') when executing the java file. \nIf you want explanation about score, add '-v' option, as first argument, when executing the file.");
        // index files
        if((args.length > 0 && (!args[0].equals("-v"))) || args.length > 1) {
            System.out.println("Process to indexing... may takes up to 1 min");
            startTime = System.currentTimeMillis();
            try {
                createIndex(analyzer);

            } catch (IOException e) {
                System.out.println(e.toString());
            }
            endTime = System.currentTimeMillis();
            diffTime = endTime - startTime;
            System.out.println("Time for indexing: "+diffTime/1000+" s.");
        }
        if(args.length > 0 && args[0].equals("-v")){
            System.out.println("Verbose activated.");
            verbose = 1;
        }
        //get query
        Scanner scan = new Scanner(System.in);  // Create a Scanner object
        System.out.println("\nEnter a query and tap Enter (just tap Enter to exit)");
        String query = scan.nextLine();  // Read user input
        while(!query.isEmpty()) {
            startTime = System.currentTimeMillis();
            //search for query
            try {
                searchQuery(query, analyzer, verbose);
            } catch (IOException e) {
                System.out.println(e.toString());
            } catch (ParseException p) {
                System.out.println(p.toString());
            }
            endTime = System.currentTimeMillis();
            diffTime = endTime - startTime;
            System.out.println("Time for query :"+diffTime+" ms.");

            System.out.println("\nEnter a query and tap Enter (just tap Enter to exit)");
            query = scan.nextLine();  // Read user input
        }

        System.out.println("Program will exit, bye.");
    }

    /* ------------------------- Indexing part ------------------------------*/


    private static void createIndex(StandardAnalyzer analyzer) throws IOException {
        String indexPath = "../Index";
        deleteDir(new File(indexPath));
        Directory indexDir = FSDirectory.open(Paths.get(indexPath));
        IndexWriterConfig writerConfig = new IndexWriterConfig(analyzer);
        IndexWriter writer = new IndexWriter(indexDir, writerConfig);
        String[] folders = {"Family", "Horror", "Scifi"};
        for(var folder : folders){
            AddContents(folder, writer);
        }
        writer.close();
    }

    private static void AddContents(String dirName, IndexWriter writer) throws IOException {
        File folder = new File("../"+dirName);
        File[] movies = folder.listFiles();
        String content= "";
        for (int i = 0; i < movies.length; i++){
            Scanner sc = new Scanner(movies[i]);
            while(sc.hasNextLine()){
                content += sc.nextLine();
            }
            addFileContent(dirName, movies[i].getName(), content, writer);
        }
    }

    private static void addFileContent(String genre, String movie, String script, IndexWriter writer) throws IOException {
        Document doc = new Document();
        String movieString = movie.replace(".txt", "");
        doc.add(new TextField("content", script, Field.Store.NO));
        doc.add(new StringField("movie", movieString , Field.Store.YES));
        doc.add(new StringField("genre", genre, Field.Store.YES));
        writer.addDocument(doc);
    }

    /* ---------------------- Delete directory in case of indexing ---------------------- */

    static boolean  deleteDir(File directoryToBeDeleted) {
        File[] allContents = directoryToBeDeleted.listFiles();
        if (allContents != null) {
            for (File file : allContents) {
                deleteDir(file);
            }
        }
        return directoryToBeDeleted.delete();
    }


    /* -------------------------- Query part --------------------------------- */

    private static void searchQuery(String query, StandardAnalyzer analyzer, int verbose) throws IOException, ParseException {
        String indexPath = "../Index";
        Directory indexDir = FSDirectory.open(Paths.get(indexPath));
        DirectoryReader reader = DirectoryReader.open(indexDir);
        IndexSearcher searcher = new IndexSearcher(reader);
        Query q = new QueryParser("content", analyzer).parse(query);
        TopScoreDocCollector collector = TopScoreDocCollector.create(10, 10);
        searcher.search(q, collector);
        ScoreDoc[] resultDocs = collector.topDocs().scoreDocs;
        for (int i = 0; i < resultDocs.length; ++i){
            int docId = resultDocs[i].doc;
            Document doc = searcher.doc(docId);
            Explanation explanation = searcher.explain(q, docId);

            String movie = doc.get("movie");
            String genre = doc.get("genre");
            float score = resultDocs[i].score;
            System.out.println((i+1) + ". " + movie + " (" + genre + ")"+"\t\t score = "+score);
            if(verbose == 1) {
                System.out.println("\nWhy this movie?");
                System.out.println(explanation.toString());
                System.out.println("\n");
            }

        }
    }

}

